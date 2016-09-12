try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('CODEPYGMENTS_EXTENSION_CONFIG', {})


MAX_SIZE = config.get('MAX_SIZE', 65536)
