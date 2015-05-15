# -*- coding: utf-8 -*-
"""Configuration object for the mfr_tabular module."""

from .libs import (
    csv_pandas,
    tsv_pandas,
    dta_pandas,
    sav_pandas,
    xlsx_xlrd
)

"""Defines a list of functions that can handle a particular file type. The
functions will be attempted in order, failing if they do not have the
requirements. Max size is the largest number of columns or rows allowed in a
single table """
#TODO: fix .dta and build .ods extensions
defaults={
    'libs': {
        '.csv': [csv_pandas],
        '.tsv': [tsv_pandas],
        '.xlsx': [xlsx_xlrd],
        '.xls': [xlsx_xlrd],
        '.dta': [dta_pandas],
        '.sav': [sav_pandas],
        # '.ods': [ods_ezodf],
    },
    'max_size': 10000,
    'table_width': 700,  # pixels
    'table_height': 600,  # pixels
    'slick_grid_options': {
        'small_table': {
            'enableCellNavigation': True,
            'enableColumnReorder': False,
            'forceFitColumns': True,
            'syncColumnCellResize': True,
        },
        'big_table': {
            'enableCellNavigation': True,
            'enableColumnReorder': False,
            'syncColumnCellResize': True,
        },
    },
}

MAX_SIZE = 10000
TABLE_WIDTH = 700
TABLE_HEIGHT = 600
