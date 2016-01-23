try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('IMAGE_EXTENSION_CONFIG', {})

TYPE = config.get('TYPE', 'jpeg')
MAXIMUM_SIZE = config.get('MAXIMUM_SIZE', '1200x1200')
