import xlrd
from collections import OrderedDict
from ..exceptions import TableTooBigException

from ..utilities import header_population
from mfr.extensions.tabular.compat import range, basestring


def xlsx_xlrd(fp):
    """Read and convert a xlsx file to JSON format using the xlrd library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    max_size = 10000

    wb = xlrd.open_workbook(fp.name)

    sheets = OrderedDict()

    for sheet in wb.sheets():
        if sheet.ncols > max_size or sheet.nrows > max_size:
            raise TableTooBigException("Table is too large to render.")

        if sheet.ncols < 1 or sheet.nrows < 1:
            sheets[sheet.name] = ([], [])
            continue

        fields = sheet.row_values(0) if sheet.nrows else []

        fields = [
            str(value)
            if not isinstance(value, basestring) and value is not None
            else value or 'Unnamed: {0}'.format(index + 1)
            for index, value in enumerate(fields)
        ]

        data = [
            dict(zip(fields, sheet.row_values(row_index)))
            for row_index in range(1, sheet.nrows)
        ]

        header = header_population(fields)
        sheets[sheet.name] = (header, data)

    return sheets
