from mfr.extensions.tabular import libs


try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('TABULAR_EXTENSION_CONFIG', {})


MAX_SIZE = config.get('MAX_SIZE', 10000)
TABLE_WIDTH = config.get('TABLE_WIDTH', 700)
TABLE_HEIGHT = config.get('TABLE_HEIGHT', 600)

LIBS = config.get('LIBS', {
    '.csv': [libs.csv_stdlib],
    '.tsv': [libs.csv_stdlib],
    '.xlsx': [libs.xlsx_xlrd],
    '.xls': [libs.xlsx_xlrd],
    '.dta': [libs.dta_pandas],
    '.sav': [libs.sav_pandas],
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
