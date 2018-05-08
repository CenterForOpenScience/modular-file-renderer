from mfr import settings

config = settings.child('PDB_EXTENSION_CONFIG')

OPTIONS = config.get_object('OPTIONS', {
    'width': 'auto',
    'height': '400',
    'antialias': True,
    'outline': True,
    'quality': 'medium',
    'fog': False
})
