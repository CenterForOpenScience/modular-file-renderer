import os

try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('UNOCONV_EXTENSION_CONFIG', {})

UNOCONV_BIN = config.get('UNOCONV_BIN', '/usr/bin/unoconv')

ADDRESS = config.get('SERVER', os.environ.get('UNOCONV_PORT_2002_TCP_ADDR', '127.0.0.1'))
PORT = config.get('PORT', os.environ.get('UNOCONV_PORT_2002_TCP_PORT', '2002'))

DEFAULT_RENDER = {'renderer': '.pdf', 'format': 'pdf'}

RENDER_MAP = config.get('RENDER_MAP', {
    # 'csv': {'renderer': '.xlsx', 'format': 'xlsx'},
    # 'ppt': {'renderer': '.pdf', 'format': 'pdf'},
    # 'pptx': {'renderer': '.pdf', 'format': 'pdf'},
})
