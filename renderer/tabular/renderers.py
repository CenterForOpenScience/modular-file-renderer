import pandas as pd
import xlrd
import rpy2.robjects as robjects
import pandas.rpy.common as com
import os
from .base import TabularRenderer
from .utilities import TooBigError, MAX_COLS, MAX_ROWS

class CSVRenderer(TabularRenderer):
    def detect(self, file_pointer):
        if file_pointer.name.endswith('.csv'):
            return True
        return False

    def _build_df(self, file_pointer):
        return pd.read_csv(file_pointer)


class STATARenderer(TabularRenderer):
    def detect(self, file_pointer):
        if file_pointer.name.endswith('.dta'):
            return True
        return False

    def _build_df(self, file_pointer):
        return pd.read_stata(file_pointer)


class ExcelRenderer(TabularRenderer):
    def detect(self, file_pointer):
        for ext in ['.xls', '.xlsx']:
            if file_pointer.name.endswith(ext):
                return True
        return False

    def _build_df(self, file_pointer):
        workbook = xlrd.open_workbook(file_pointer.name)
        sheets = workbook.sheet_names()
        sheet = workbook.sheet_by_name(sheets[0])
        if sheet.ncols >MAX_COLS or sheet.nrows > MAX_ROWS:
            raise TooBigError
        return pd.read_excel(file_pointer, sheets[0])


class SPSSRenderer(TabularRenderer):
    def detect(self, file_pointer):
        if file_pointer.name.endswith('.sav'):
            return True
        return False

    def _build_df(self, file_pointer):
        r = robjects
        r.r("require(foreign)")
        r.r('x <- read.spss("{}",to.data.frame=T)'.format(file_pointer.name))
        r.r('row.names(x) = 0:(nrow(x)-1)')
        return com.load_data('x')