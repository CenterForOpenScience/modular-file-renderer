try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('CODEPYGMENTS_EXTENSION_CONFIG', {})


PYGMENTS_THEME = config.get('PYGMENTS_THEME', 'default.css')
CSS_CLASS = config.get('CSS_CLASS', 'codehilite')
