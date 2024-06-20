import uuid
from collections import OrderedDict

import xlrd

from mfr.extensions.tabular.compat import range, basestring
from mfr.extensions.tabular.utilities import header_population
from mfr.extensions.tabular.exceptions import TableTooBigError


def xlsx_xlrd(fp, max_iterations=5000):
    """Read and convert a xlsx file to JSON format using the xlrd library.
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    max_size = 10000

    wb = xlrd.open_workbook(fp.name)

    sheets = OrderedDict()

    for sheet in wb.sheets():
        if sheet.ncols > max_size or sheet.nrows > max_size:
            raise TableTooBigError('Table is too large to render.', '.xlsx',
                                   nbr_cols=sheet.ncols, nbr_rows=sheet.nrows)

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

        # Duplicate header fields create errors, we need to rename them
        duplicate_fields = set([x for x in fields if fields.count(x) > 1])
        if len(duplicate_fields):
            counts = {}
            for field in duplicate_fields:
                counts[field] = 1

            for i, field in enumerate(fields):
                if field in duplicate_fields:
                    increased_name = field + ' ({})'.format(counts[field])

                    # this triggers if you try to rename a header, and that new name
                    # already exists in fields. it will then increment to look for the
                    # next available name.
                    iteration = 0
                    while increased_name in fields:
                        iteration += 1
                        if iteration > max_iterations:
                            increased_name = field + ' ({})'.format(uuid.uuid4())
                        else:
                            counts[field] += 1
                            increased_name = field + ' ({})'.format(counts[field])

                    fields[i] = increased_name
        data = []
        for i in range(1, sheet.nrows):
            row = []
            for cell in sheet.row(i):
                if cell.ctype == xlrd.XL_CELL_DATE:
                    value = xlrd.xldate.xldate_as_datetime(cell.value, wb.datemode).isoformat()
                else:
                    value = cell.value
                row.append(value)
            data.append(dict(zip(fields, row)))

        header = header_population(fields)
        sheets[sheet.name] = (header, data)

    return sheets
