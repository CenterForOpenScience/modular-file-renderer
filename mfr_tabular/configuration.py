# -*- coding: utf-8 -*-
"""Configuration object for the mfr_tabular module."""

from .libs import (
    csv_csv,
    csv_pandas,
    dta_pandas,
    sav_pandas,
    xlsx_xlrd
)

from mfr import Config


"""Defines a list of functions that can handle a particular file type. The
functions will be attempted in order, failing if they do not have the
requirements. Max size is the largest number of columns or rows allowed in a
single table"""
config = Config(defaults={
    'libs': {
        '.csv': [csv_pandas, csv_csv],
        '.tsv': [csv_csv],
        '.xlsx': [xlsx_xlrd],
        '.xls': [xlsx_xlrd],
        '.dta': [dta_pandas],
        '.sav': [sav_pandas],
        # '.ods': [ods_ezodf],
    },
    'max_size': 10000,
    'table_width': 600,  # pixels
    'table_height': 600,  # pixels
})
