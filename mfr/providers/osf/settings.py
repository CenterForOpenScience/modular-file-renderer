try:
    from waterbutler import settings
except ImportError:
    settings = {}

config = settings.get('OSF_PROVIDER_CONFIG', {})


# BASE_URL = config.get('BASE_URL', 'http://localhost:5001/')
