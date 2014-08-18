"""Imports a function from the correct library. This structure allows the
function name to be passed without initializing its module and without breaking
if the module's requirements are not met. """


def csv_csv():
    from csv_tools import csv_csv
    return csv_csv


def csv_pandas():
    from panda_tools import csv_pandas
    return csv_pandas


def dta_pandas():
    from panda_tools import dta_pandas
    return dta_pandas


def sav_pandas():
    from panda_tools import sav_pandas
    return sav_pandas


def xlsx_xlrd():
    from xlrd_tools import xlsx_xlrd
    return xlsx_xlrd
