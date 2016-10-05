from mfr import settings
from mfr.extensions.tabular import libs

config = settings.child('TABULAR_EXTENSION_CONFIG')

MAX_SIZE = config.get('MAX_SIZE', 10000)
TABLE_WIDTH = config.get('TABLE_WIDTH', 700)
TABLE_HEIGHT = config.get('TABLE_HEIGHT', 600)

LIBS = config.get('LIBS', {
    '.csv': [libs.csv_stdlib],
    '.tsv': [libs.csv_stdlib],
    '.gsheet': [libs.xlsx_xlrd],
    '.xlsx': [libs.xlsx_xlrd],
    '.xls': [libs.xlsx_xlrd],
    '.dta': [libs.dta_pandas],
    '.sav': [libs.sav_stdlib],
    # '.ods': [libs.ods_ezodf],
})

SMALL_TABLE = config.get('SMALL_TABLE', {
    'enableCellNavigation': True,
    'enableColumnReorder': False,
    'forceFitColumns': True,
    'syncColumnCellResize': True,
    'multiColumnSort': True,
})

BIG_TABLE = config.get('BIG_TABLE', {
    'enableCellNavigation': True,
    'enableColumnReorder': False,
    'syncColumnCellResize': True,
    'multiColumnSort': True,
})

PSPP_CONVERT_BIN = config.get('PSPP_CONVERT_BIN', '/usr/bin/pspp-convert')
