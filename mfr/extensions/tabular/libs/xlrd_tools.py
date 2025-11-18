import xlrd
import zipfile

from io import BytesIO
from openpyxl import load_workbook
from collections import OrderedDict
from ..utilities import (
    to_bytes,
    parse_xls,
    parse_xlsx
)


def xls(fp):
    """
    .xls → xlrd; supports truncation and optional meta collection.
    """
    sheets = OrderedDict()
    wb = xlrd.open_workbook(file_contents=to_bytes(fp))
    return parse_xls(wb, sheets)

def xlsx(fp):
    """
    .xlsx → openpyxl; supports truncation and optional meta collection.
    """
    sheets = OrderedDict()
    try:
        wb = load_workbook(BytesIO(to_bytes(fp)), data_only=True, read_only=True)
    except zipfile.BadZipFile as exc:
        raise xlrd.biffh.XLRDError(
            "Invalid xlsx file or corrupted ZIP structure"
        ) from exc

    return parse_xlsx(wb, sheets)
