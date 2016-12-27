from mfr.core.exceptions import RendererError


class MissingRequirementsError(RendererError):
    def __init__(self, message, function_preference, renderer_class: str,
                 extension: str, code: int=500):

        self.keen_data = {'function_preference': function_preference}

        super().__init__(message, 'missing_requirements', renderer_class,
                         extension, code=code)


class EmptyTableError(RendererError):
    def __init__(self, message, renderer_class: str,
                 extension: str, code: int=500):

        self.keen_data = {}

        super().__init__(message, 'empty_table', renderer_class,
                         extension, code=code)


class TableTooBigError(RendererError):
    def __init__(self, message, renderer_class: str,
                 extension: str, code: int=500):

        self.keen_data = {}

        super().__init__(message, 'table_too_big', renderer_class,
                         extension, code=code)


class UnexpectedFormattingError(RendererError):
    def __init__(self, message, formatting_function: str, renderer_class: str,
                 extension: str, code: int=500):

        self.keen_data = {'formatting_function': formatting_function}

        super().__init__(message, 'unexpected_formatting', renderer_class,
                         extension, code=code)
