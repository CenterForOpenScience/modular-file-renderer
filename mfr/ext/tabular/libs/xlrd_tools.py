import xlrd
from ..exceptions import TableTooBigException, EmptyTableException
from ..configuration import config
from ..utilities import header_population
from ..compat import range


def xlsx_xlrd(fp):
    """Read and convert a xlsx file to JSON format using the xlrd library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """

    max_size = config['max_size']

    wb = xlrd.open_workbook(fp.name)

    # Currently only displays the first sheet if there are more than one.
    sheet = wb.sheets()[0]

    if sheet.ncols > max_size or sheet.nrows > max_size:
        raise TableTooBigException("Table is too large to render.")

    if sheet.ncols < 1 or sheet.nrows < 1:
        raise EmptyTableException("Table is empty or corrupt.")

    fields = sheet.row_values(0) if sheet.nrows else []

    fields = [str(value).encode('ascii', 'ignore') or 'Unnamed: {0}'.format(index+1) for index, value in enumerate(fields)]

    data = [dict(zip(fields, sheet.row_values(row_index)))
        for row_index in range(1, sheet.nrows)]

    header = header_population(fields)

    return header, data
