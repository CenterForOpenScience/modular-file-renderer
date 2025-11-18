import copy
import types
from dataclasses import is_dataclass, fields

import kombu.utils.json

__registry = {}

_ATOMIC_TYPES = frozenset({
    # Common JSON Serializable types
    types.NoneType,
    bool,
    int,
    float,
    str,
    # Other common types
    complex,
    bytes,
    # Other types that are also unaffected by deepcopy
    types.EllipsisType,
    types.NotImplementedType,
    types.CodeType,
    types.BuiltinFunctionType,
    types.FunctionType,
    type,
    range,
    property,
})


def serialize(obj, *, dict_factory=dict):
    if not is_dataclass(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(obj, dict_factory):
    obj_type = type(obj)
    if obj_type in _ATOMIC_TYPES:
        return obj
    elif is_dataclass(obj_type):
        # dataclass instance: fast path for the common case
        if obj_type.__name__ not in __registry:
            raise TypeError('cannot serialize non-serializable class')
        if dict_factory is dict:
            return {
                f.name: _asdict_inner(getattr(obj, f.name), dict)
                for f in fields(obj)
            } | {'__type': obj_type.__name__}
        else:
            return dict_factory([
                (f.name, _asdict_inner(getattr(obj, f.name), dict_factory))
                for f in fields(obj)
            ]) | {'__type': obj_type.__name__}
    elif obj_type is list:
        return [_asdict_inner(v, dict_factory) for v in obj]
    elif obj_type is dict:
        return {
            _asdict_inner(k, dict_factory): _asdict_inner(v, dict_factory)
            for k, v in obj.items()
        }
    elif obj_type is tuple:
        return tuple([_asdict_inner(v, dict_factory) for v in obj])
    elif issubclass(obj_type, tuple):
        if hasattr(obj, '_fields'):
            return obj_type(*[_asdict_inner(v, dict_factory) for v in obj])
        else:
            return obj_type(_asdict_inner(v, dict_factory) for v in obj)
    elif issubclass(obj_type, dict):
        if hasattr(obj_type, 'default_factory'):
            result = obj_type(obj.default_factory)
            for k, v in obj.items():
                result[_asdict_inner(k, dict_factory)] = _asdict_inner(v, dict_factory)
            return result
        return obj_type((_asdict_inner(k, dict_factory),
                         _asdict_inner(v, dict_factory))
                        for k, v in obj.items())
    elif issubclass(obj_type, list):
        return obj_type(_asdict_inner(v, dict_factory) for v in obj)
    else:
        return copy.deepcopy(obj)


def serializable(cls):
    assert is_dataclass(cls), f'class {cls.__name__} is not a dataclass, therefore cannot be serializable'
    assert cls.__name__ not in __registry, 'This class has already been registered'
    __registry[cls.__name__] = cls

    kombu.utils.json.register_type(
        cls,
        cls.__name__,
        serialize,
        deserialize,
    )
    return cls


def deserialize(data):
    if isinstance(data, list):
        return [deserialize(item) for item in data]
    if isinstance(data, dict):
        data_type = data.pop('__type', None)
        if not data_type:
            raise TypeError('invalid deserialize payload')
        if data_type not in __registry:
            raise TypeError(f'type provided but type {data_type.__name__} is not declared serializable')
        data_type = __registry.get(data_type)
        for field in fields(data_type):
            if is_dataclass(field.type) or isinstance(field.type, list):
                data[field.name] = deserialize(data[field.name])
        return data_type(**data)

    raise TypeError(f'Cannot deserialize type {type(data)}')


__all__ = ['serializable']
