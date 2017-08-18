import FreeCAD
import Part
import Mesh

import sys

in_fn, out_fn = sys.argv[2], sys.argv[3]

try:
    Part.open(in_fn)
except:
    sys.exit(1)

o = [FreeCAD.getDocument("Unnamed").findObjects()[0]]
Mesh.export(o, out_fn)
