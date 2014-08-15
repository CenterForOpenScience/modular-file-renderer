# -*- coding: utf-8 -*-
"""Configuration object for the mfr_tabular module."""

from .import_dependencies import csv_pandas, dta_pandas, sav_pandas, csv_csv, xlsx_xlrd
from mfr import Config


# Define ordered lists to indicate the preference of which library to use for
# a partocular extension.
config = Config(defaults={
    'tabular_libraries': {
        '.csv': [csv_pandas, csv_csv],
        '.tsv': [csv_csv],
        '.xlsx': [xlsx_xlrd],
        '.xls': [xlsx_xlrd],
        '.dta': [dta_pandas],
        '.sav': [sav_pandas],
        # '.ods': [ods_ezodf],
    },
    'max_size': 10000
})
