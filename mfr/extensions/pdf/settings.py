from mfr import settings


config = settings.child('PDF_EXTENSION_CONFIG')

EXPORT_TYPE = config.get('EXPORT_TYPE', 'pdf')
assert EXPORT_TYPE  # mandatory config
EXPORT_MAXIMUM_SIZE = config.get('EXPORT_MAXIMUM_SIZE', '1200x1200')

ENABLE_HYPOTHESIS = config.get_bool('ENABLE_HYPOTHESIS', True)

# supports multiple files in the form of a space separated string
EXPORT_SUPPORTED = config.get('EXPORT_SUPPORTED', '.tiff .tif').split(' ')
EXPORT_MAX_PAGES = int(config.get('EXPORT_MAX_PAGES', 40))
