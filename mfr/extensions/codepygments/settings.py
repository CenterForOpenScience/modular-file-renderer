from mfr import settings

config = settings.child('CODEPYGMENTS_EXTENSION_CONFIG')

MAX_SIZE = config.get('MAX_SIZE', 65536)
