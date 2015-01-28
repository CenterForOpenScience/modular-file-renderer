from __future__ import division
import sys

PY2 = int(sys.version[0]) == 2
PY26 = PY2 and int(sys.version_info[1]) < 7

if PY2:
    range = xrange
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
    if PY26:
        from .ordereddict import OrderedDict
    else:
        from collections import OrderedDict
    OrderedDict = OrderedDict
else:
    range = range
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)
    from collections import OrderedDict
    OrderedDict = OrderedDict
