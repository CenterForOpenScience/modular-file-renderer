"""Imports a function from the correct library. This structure allows the
function name to be passed without initializing its module and without breaking
if the module's requirements are not met. """


def csv_stdlib():
    from ..libs.stdlib_tools import csv_stdlib
    return csv_stdlib


def csv_pandas():
    from ..libs.panda_tools import csv_pandas
    return csv_pandas


def tsv_pandas():
    from ..libs.panda_tools import tsv_pandas
    return tsv_pandas


def dta_pandas():
    from ..libs.panda_tools import dta_pandas
    return dta_pandas


def sav_pandas():
    from ..libs.panda_tools import sav_pandas
    return sav_pandas


def xlsx_xlrd():
    from ..libs.xlrd_tools import xlsx_xlrd
    return xlsx_xlrd
