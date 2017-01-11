from mfr import settings

config = settings.child('CODEPYGMENTS_EXTENSION_CONFIG')

MAX_SIZE = int(config.get('MAX_SIZE', 204800))  # 200kb
