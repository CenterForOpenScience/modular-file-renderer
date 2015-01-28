from __future__ import division
import sys

PY2 = int(sys.version[0]) == 2

if PY2:
    range = xrange
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
else:
    range = range
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)
