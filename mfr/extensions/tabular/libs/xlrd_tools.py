import xlrd
import zipfile
from collections import OrderedDict
from ..exceptions import TableTooBigError, MissingRequirementsError

from ..utilities import header_population
from mfr.extensions.tabular.compat import range, basestring


def xlsx_xlrd(fp):
    """Read and convert a xlsx file to JSON format using the xlrd library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    MAX_SIZE = 10000

    try:
        wb = xlrd.open_workbook(fp.name)
        using_xlrd = True
    except xlrd.biffh.XLRDError:
        using_xlrd = False
        try:
            from openpyxl import load_workbook
        except ImportError:
            raise MissingRequirementsError(
                'openpyxl is required to read .xlsx files',
                function_preference='openpyxl'
            )
        try:
            wb = load_workbook(fp.name, data_only=True)
        except zipfile.BadZipFile:
            raise xlrd.biffh.XLRDError("Excel xlsx file; not supported")

    sheets = OrderedDict()

    if using_xlrd:
        for sheet in wb.sheets():
            if sheet.ncols > MAX_SIZE or sheet.nrows > MAX_SIZE:
                raise TableTooBigError('Table is too large to render.', '.xlsx',
                                       nbr_cols=sheet.ncols, nbr_rows=sheet.nrows)

            if sheet.ncols < 1 or sheet.nrows < 1:
                sheets[sheet.name] = ([], [])
                continue

            fields = sheet.row_values(0) if sheet.nrows else []

            fields = [
                str(value)
                if not isinstance(value, basestring) and value is not None
                else value or f'Unnamed: {index + 1}'
                for index, value in enumerate(fields)
            ]

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

    else:
        for name in wb.sheetnames:
            ws = wb[name]
            nrows = ws.max_row
            ncols = ws.max_column
            if ncols > MAX_SIZE or nrows > MAX_SIZE:
                raise TableTooBigError('Table is too large to render.', '.xlsx',
                                       nbr_cols=ncols, nbr_rows=nrows)

            if nrows < 1 or ncols < 1:
                sheets[name] = ([], [])
                continue

            header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
            fields = [
                str(val) if val is not None else f'Unnamed: {i+1}'
                for i, val in enumerate(header_row)
            ]

            data = []
            for row in ws.iter_rows(min_row=2, max_row=nrows, max_col=ncols, values_only=True):
                data.append(dict(zip(fields, row)))

            header = header_population(fields)
            sheets[name] = (header, data)

    return sheets
