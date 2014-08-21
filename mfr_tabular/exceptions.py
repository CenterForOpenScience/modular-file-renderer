from mfr.exceptions import RenderError


class MissingRequirementsException(RenderError):
    pass


class EmptyTableException(RenderError):
    pass


class TableTooBigException(RenderError):
    pass
