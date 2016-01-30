from mfr.core.exceptions import RendererError


class MissingRequirementsException(RendererError):
    pass


class EmptyTableException(RendererError):
    pass


class TableTooBigException(RendererError):
    pass


class UnexpectedFormattingException(RendererError):
    pass
