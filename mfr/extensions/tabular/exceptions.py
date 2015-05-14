from mfr._exceptions import RenderError


class MissingRequirementsException(RenderError):
    pass


class EmptyTableException(RenderError):
    pass


class TableTooBigException(RenderError):
    pass


class UnexpectedFormattingException(RenderError):
    pass
