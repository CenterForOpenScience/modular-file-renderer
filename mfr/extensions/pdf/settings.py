from mfr import settings


config = settings.child('PDF_EXTENSION_CONFIG')

EXPORT_TYPE = config.get('EXPORT_TYPE', 'pdf')
EXPORT_MAXIMUM_SIZE = config.get('EXPORT_MAXIMUM_SIZE', '1200x1200')
EXPORT_EXCLUSIONS = config.get('EXPORT_EXCLUSIONS', ['.pdf', ])
