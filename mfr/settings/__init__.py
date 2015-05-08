from .defaults import *

try:
    from .local import *
except ImportError as error:
    raise ImportError("No local.py settings file found. Did you remember to "
                        "copy local-dist.py to local.py?")
