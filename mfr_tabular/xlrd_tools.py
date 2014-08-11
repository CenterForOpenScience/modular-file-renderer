from dependencies import xlrd
from utilities import header_population


def data_from_xlrd(fp):

    wb = xlrd.open_workbook(fp.name)

    # Currently only displays the first sheet if there are more than one.
    sheet = wb.sheets()[0]

    fields = sheet.row_values(0) if sheet.nrows else []

    data = [dict(zip(fields, sheet.row_values(row_index)))
            for row_index in xrange(1, sheet.nrows)]

    header = header_population(fields)

    return header, data
