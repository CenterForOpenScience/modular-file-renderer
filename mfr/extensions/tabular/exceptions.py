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

    def __init__(self, message, *args, code: int=400, nbr_cols: int=0, nbr_rows: int=0, **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.nbr_cols = nbr_cols
        self.nbr_rows = nbr_rows
        self.attr_stack.append([self.__TYPE, {
            'nbr_cols': self.nbr_cols,
            'nbr_rows': self.nbr_rows
        }])


class UnexpectedFormattingError(TabularRendererError):

    __TYPE = 'tabular_unexpected_formatting'

    def __init__(self, message, *args, code: int=500, formatting_function: str='', **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.formatting_function = formatting_function
        self.attr_stack.append([self.__TYPE, {'formatting_function': self.formatting_function}])


class FileTooLargeError(TabularRendererError):

    __TYPE = 'tabular_file_too_large'

    def __init__(self, message, *args, code: int=400, file_size: int=None, max_size: int=None,
                 **kwargs):
        super().__init__(message, *args, code=code, **kwargs)

        self.file_size = file_size
        self.max_size = max_size

        self.attr_stack.append([self.__TYPE, {
            'file_size': self.file_size,
            'max_size': self.max_size
        }])
