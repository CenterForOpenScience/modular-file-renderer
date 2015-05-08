IDENTITY_METHODS = {}


def get_identity_func(name):
    try:
        return IDENTITY_METHODS[name]
    except KeyError:
        raise NotImplementedError('No identity getter for {0}'.format(name))


def get_identity(name, **kwargs):
    return get_identity_func(name)(**kwargs)


