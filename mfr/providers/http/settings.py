try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('HTTP_PROVIDER_CONFIG', {})
