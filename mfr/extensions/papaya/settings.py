from mfr import settings

config = settings.child('PAPAYA_EXTENSION_CONFIG')

# Directory to temporarily store papaya image files
DATA_DIR = 'mfr/extensions/papaya/static/data/'
# Files older then this many seconds will be deleted from DATA_DIR at the beggining of each render.
DATA_OLD = 300
