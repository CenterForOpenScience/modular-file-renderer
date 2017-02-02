from mfr.core.exceptions import RendererError

class TabularRendererError(RendererError):

    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, renderer_class='tabular', **kwargs)


class MissingRequirementsError(TabularRendererError):

    __TYPE = 'tabular_missing_requirements'

    def __init__(self, message, *args, code: int=500, function_preference: str='', **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.function_preference = function_preference
        self.attr_stack.append([self.__TYPE, {'function_preference': self.function_preference}])


class EmptyTableError(TabularRendererError):

    __TYPE = 'tabular_empty_table'

    def __init__(self, message, *args, code: int=400, **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.attr_stack.append([self.__TYPE, {}])


class TableTooBigError(TabularRendererError):

    __TYPE = 'tabular_table_too_big'

    def __init__(self, message, *args, code: int=400, **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.attr_stack.append([self.__TYPE, {}])

class TooBigToRenderError(TabularRendererError):

    __TYPE = 'tabular_too_big_to_render'

    def __init__(self, message, *args, code: int=400, **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.attr_stack.append([self.__TYPE, {}])


class UnexpectedFormattingError(TabularRendererError):

    __TYPE = 'tabular_unexpected_formatting'

    def __init__(self, message, *args, code: int=500, formatting_function: str='', **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.formatting_function = formatting_function
        self.attr_stack.append([self.__TYPE, {'formatting_function': self.formatting_function}])
