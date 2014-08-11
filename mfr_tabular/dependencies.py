try:
    import pandas
except ImportError:
    pandas = None

try:
    import xlrd
except ImportError:
    xlrd = None

try:
    import rpy2.robjects as robjects
except ImportError:
    robjects = None

try:
    import pandas.rpy.common as common
except ImportError:
    common = None

try:
    import ezodf
except ImportError:
    ezodf = None
