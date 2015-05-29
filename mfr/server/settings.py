import hashlib

try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('SERVER_CONFIG', {})


ADDRESS = config.get('ADDRESS', '127.0.0.1')
PORT = config.get('PORT', 7778)

DEBUG = config.get('DEBUG', True)

SSL_CERT_FILE = config.get('SSL_CERT_FILE', None)
SSL_KEY_FILE = config.get('SSL_KEY_FILE', None)

XHEADERS = config.get('XHEADERS', False)
CORS_ALLOW_ORIGIN = config.get('CORS_ALLOW_ORIGIN', '*')

CHUNK_SIZE = config.get('CHUNK_SIZE', 65536)  # 64KB
MAX_BUFFER_SIZE = config.get('MAX_BUFFER_SIZE', 1024 * 1024 * 100)  # 100MB

IDENTITY_METHOD = config.get('IDENTITY_METHOD', 'rest')
IDENTITY_API_URL = config.get('IDENTITY_API_URL', 'http://127.0.0.1:5001/api/v1/files/auth/')

HMAC_ALGORITHM = getattr(hashlib, config.get('HMAC_ALGORITHM', 'sha256'))
HMAC_SECRET = config.get('HMAC_SECRET', 'changeme').encode('utf-8')

PROVIDER_NAME = config.get('PROVIDER_NAME', 'osf')

CACHE_ENABLED = config.get('CACHE_ENABLED', False)
CACHE_PROVIDER_NAME = config.get('CACHE_PROVIDER_NAME', 'filesystem')
CACHE_PROVIDER_SETTINGS = config.get('CACHE_PROVIDER_SETTINGS', {'folder': '/tmp/mfr/'})
CACHE_PROVIDER_CREDENTIALS = config.get('CACHE_PROVIDER_CREDENTIALS', {})

LOCAL_CACHE_PROVIDER_SETTINGS = config.get('LOCAL_CACHE_PROVIDER_SETTINGS', {'folder': '/tmp/mfrlocalcache/'})
