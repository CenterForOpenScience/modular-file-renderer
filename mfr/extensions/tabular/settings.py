from mfr import settings
from mfr.extensions.tabular import libs


config = settings.child('TABULAR_EXTENSION_CONFIG')

MAX_FILE_SIZE = int(config.get('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10Mb
MAX_SIZE = int(config.get('MAX_SIZE', 10000))  # max number of rows or columns allowed.
TABLE_WIDTH = int(config.get('TABLE_WIDTH', 700))
TABLE_HEIGHT = int(config.get('TABLE_HEIGHT', 600))

LIBS = config.get_object('LIBS', {
    '.csv': [libs.csv_stdlib],
    '.tsv': [libs.csv_stdlib],
    '.gsheet': [libs.xlsx_xlrd],
    '.xlsx': [libs.xlsx_xlrd],
    '.xls': [libs.xlsx_xlrd],
    '.dta': [libs.dta_pandas],
    '.sav': [libs.sav_stdlib],
    '.mat': [libs.mat_h5py_scipy],
    # '.ods': [libs.ods_ezodf],
})

SMALL_TABLE = config.get_object('SMALL_TABLE', {
    'enableCellNavigation': True,
    'enableColumnReorder': False,
    'forceFitColumns': True,
    'syncColumnCellResize': True,
    'multiColumnSort': True,
})

BIG_TABLE = config.get_object('BIG_TABLE', {
    'enableCellNavigation': True,
    'enableColumnReorder': False,
    'syncColumnCellResize': True,
    'multiColumnSort': True,
})

PSPP_CONVERT_BIN = config.get('PSPP_CONVERT_BIN', '/usr/bin/pspp-convert')
PSPP_CONVERT_TIMEOUT = int(config.get('PSPP_CONVERT_TIMEOUT', 30))  # In seconds
