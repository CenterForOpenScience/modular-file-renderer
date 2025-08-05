import os

from mfr import settings

config = settings.child("UNOSERVER_EXTENSION_CONFIG")

UNOSERVER_TIMEOUT = int(config.get("TIMEOUT", 60))

UNOSERVER_HOST = config.get("HOST", os.environ.get("UNOSERVER_INTERFACE", "127.0.0.1"))
UNOSERVER_PORT = config.get("PORT", os.environ.get("UNOSERVER_PORT", "2003"))
DEFAULT_RENDER = {"renderer": ".pdf", "format": "pdf"}

RENDER_MAP = config.get_object(
    "RENDER_MAP",
    {
        # "csv": {"renderer": ".xlsx", "format": "xlsx"},
        # "ppt": {"renderer": ".pdf", "format": "pdf"},
        # "pptx": {"renderer": ".pdf", "format": "pdf"},
    },
)
