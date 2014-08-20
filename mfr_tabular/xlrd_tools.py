import xlrd
from .utilities import header_population
from .compat import range


def xlsx_xlrd(fp):
    """Read and convert a xlsx file to JSON format using the xlrd library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """

    wb = xlrd.open_workbook(fp.name)

    # Currently only displays the first sheet if there are more than one.
    sheet = wb.sheets()[0]

    fields = sheet.row_values(0) if sheet.nrows else []

    data = [dict(zip(fields, sheet.row_values(row_index)))
            for row_index in range(1, sheet.nrows)]

    header = header_population(fields)

    return header, data
