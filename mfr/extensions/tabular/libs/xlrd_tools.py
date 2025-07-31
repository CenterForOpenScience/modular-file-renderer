import zipfile
from collections import OrderedDict
from io import BytesIO

import xlrd
from openpyxl import load_workbook

from ..utilities import parse_xls, parse_xlsx, to_bytes


def xlsx_xlrd(fp):
    """
    • .xls → xlrd
    • .xlsx → openpyxl (xlrd ≥2.0 dropped xlsx support)

    `fp` is the stream returned by WaterButler/MFR.  It may already have been
    read, so we always rewind and copy to an in‑memory buffer that openpyxl (and
    ZipFile) can seek inside safely.
    """
    sheets = OrderedDict()

    try:
        wb = xlrd.open_workbook(file_contents=to_bytes(fp))
        return parse_xls(wb, sheets)
    except xlrd.biffh.XLRDError:
        pass

    try:
        wb = load_workbook(BytesIO(to_bytes(fp)), data_only=True, read_only=True)
    except zipfile.BadZipFile as exc:
        raise xlrd.biffh.XLRDError("Invalid xlsx file or corrupted ZIP structure") from exc

    return parse_xlsx(wb, sheets)
