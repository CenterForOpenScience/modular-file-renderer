import sys

import Mesh
import Part
import FreeCAD

# This file is run by Freecads own version of python to do step file conversion
# The exporter will shell out to Freecad and provide the path to this file

in_fn, out_fn = sys.argv[2], sys.argv[3]

try:
    Part.open(in_fn)
except:
    sys.exit(1)

o = [FreeCAD.getDocument("Unnamed").findObjects()[0]]
Mesh.export(o, out_fn)
