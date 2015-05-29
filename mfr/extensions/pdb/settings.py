try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('PDB_EXTENSION_CONFIG', {})


MIN_HEIGHT = config.get('MIN_HEIGHT', '500px')
MIN_WIDTH = config.get('MIN_WIDTH', '100%')

OPTIONS = config.get('OPTIONS', {
    'width': 'auto',
    'height': 'auto',
    'antialias': True,
    'outline': True,
    'quality': 'medium',
    'fog': False
})
