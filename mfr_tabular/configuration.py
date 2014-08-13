# -*- coding: utf-8 -*-
"""Configuration object for the mfr_tabular module."""

from .panda_tools import csv_pandas, dta_pandas, sav_pandas
from .csv_tools import csv_csv
# from .ezodf_tools import ods_ezodf
from .xlrd_tools import xlsx_xlrd
from mfr import Config

# Define ordered lists to indicate the preference of which library to use for
# a partocular extension.
config = Config(defaults={
    'tabular_libraries': {
        '.csv': [csv_pandas, csv_csv],
        '.tsv': [csv_csv],
        '.xlsx': [xlsx_xlrd],
        '.dta': [dta_pandas],
        '.sav': [sav_pandas],
        # '.ods': [ods_ezodf],
    },
    'max_size': 10000
})
