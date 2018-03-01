from mfr import settings

config = settings.child('IMAGE_EXTENSION_CONFIG')

EXPORT_TYPE = config.get('EXPORT_TYPE', 'jpeg')
EXPORT_MAXIMUM_SIZE = config.get('EXPORT_MAXIMUM_SIZE', '2400x2400')
EXPORT_EXCLUSIONS = config.get('EXPORT_EXCLUSIONS', '.gif .ico').split(' ')
EXPORT_BACKGROUND_COLOR = config.get('EXPORT_BACKGROUND_COLOR', 'white')
