import sys

PY2 = int(sys.version[0]) == 2

if PY2:
    range = xrange
else:
    range = range
