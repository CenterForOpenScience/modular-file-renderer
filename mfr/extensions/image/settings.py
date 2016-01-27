try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('IMAGE_EXTENSION_CONFIG', {})

EXPORT_TYPE = config.get('EXPORT_TYPE', 'jpeg')
EXPORT_MAXIMUM_SIZE = config.get('EXPORT_MAXIMUM_SIZE', '1200x1200')
EXPORT_EXCLUSIONS = config.get('EXPORT_EXCLUSIONS', ['.gif', '.ico', ])
