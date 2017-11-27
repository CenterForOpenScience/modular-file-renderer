from mfr import settings

config = settings.child('JSC3D_EXTENSION_CONFIG')

FREECAD_BIN = config.get('FREECAD_BIN', '/usr/bin/freecadcmd')
FREECAD_CONVERT_SCRIPT = config.get('FREECAD_CONVERT_SCRIPT', '/code/mfr/extensions/jsc3d/freecad_converter.py')
EXPORT_TYPE = config.get('EXPORT_TYPE', '.stl')
EXPORT_EXCLUSIONS = config.get('EXPORT_EXCLUSIONS', '.3ds .stl .obj .ctm').split(' ')
