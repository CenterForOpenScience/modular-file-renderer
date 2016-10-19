from mfr.core.exceptions import RendererError


class FileTooLargeException(RendererError):
    def __init__(self, *args, **kwargs):
        super().__init__(code=400, *args, **kwargs)
