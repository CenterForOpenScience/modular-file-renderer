try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('PDB_EXTENSION_CONFIG', {})


OPTIONS = config.get('OPTIONS', {
    'width': 'auto',
    'height': '600',
    'antialias': True,
    'outline': True,
    'quality': 'medium',
    'fog': False
})
