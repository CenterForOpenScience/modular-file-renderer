import re
import xlrd

from http import HTTPStatus
from subprocess import (check_call,
                        TimeoutExpired,
                        CalledProcessError)
from tempfile import NamedTemporaryFile

from mfr.extensions.tabular import compat
from mfr.core.exceptions import SubprocessError, CorruptedError
from mfr.extensions.tabular.settings import (PSPP_CONVERT_BIN,
                                             PSPP_CONVERT_TIMEOUT,
                                             MAX_SIZE)


def header_population(headers):
    """make column headers from a list
    :param headers: list of column headers
    :return: a list of dictionaries
    """
    return [{'id': field, 'name': field, 'field': field, 'sortable': True} for field in headers]


def data_population(in_data, headers=None):
    """Convert a list of lists into a list of dicts associating each
    cell with its column header and row
    :param in_data: two dimensional list of data
    :param headers: column headers
    :return: JSON representation of rows
    """
    headers = headers or in_data[0]

    return [
        {header: row[cindex]
            for cindex, header in enumerate(headers)}
        for row in in_data
    ]


def strip_comments(src, dest):
    data = re.sub('%.*?\n', '', src.read())
    # Destination temp file is opened in binary mode; must cast contents to
    # bytes before writing.
    if isinstance(data, compat.unicode):
        data = data.encode('utf-8', 'ignore')
    dest.write(data)
    dest.seek(0)


def sav_to_csv(fp):
    """Converts a SPSS .sav to a .csv file by calling out to ``pspp-convert``.

    :param fp: file pointer object to .sav file
    :return: file pointer to .csv file. You are responsible for closing this.
    """
    csv_file = NamedTemporaryFile(mode='w+b', suffix='.csv')
    try:
        check_call(
            [PSPP_CONVERT_BIN, fp.name, csv_file.name],
            timeout=PSPP_CONVERT_TIMEOUT,
        )
    except CalledProcessError as err:
        raise SubprocessError(
            'Unable to convert the SPSS file to CSV, please try again later.',
            code=HTTPStatus.INTERNAL_SERVER_ERROR,
            process='pspp',
            cmd=str(err.cmd),
            returncode=err.returncode,
            path=fp.name,
            extension='sav',
            exporter_class='tabular',
        )
    except TimeoutExpired as err:
        # The return code 52 is not the error code returned by the
        # subprocess, but the error given to it by this waterbutler
        # processs, for timing out.
        raise SubprocessError(
            'CSV Conversion timed out.',
            code=HTTPStatus.GATEWAY_TIMEOUT,
            process='pspp',
            cmd=str(err.cmd),
            returncode=52,
            path=fp.name,
            extension='sav',
            exporter_class='tabular'
        )
    return csv_file


def to_bytes(fp):
    """
    Return *exactly* the original bytes of the Excel file and rewind *fp*.
    Handles both binary and text wrappers that WaterButler may give us.
    """
    try:
        fp.seek(0)
    except Exception:
        pass

    raw = fp.read()
    if isinstance(raw, bytes):
        try:
            fp.seek(0)
        except Exception:
            pass
        return raw

    if hasattr(fp, "buffer"):
        buf = fp.buffer
        try:
            buf.seek(0)
        except Exception:
            pass
        data = buf.read()
        try:
            buf.seek(0)
        except Exception:
            pass
    else:
        data = raw.encode("utf-8", "surrogateescape")

    try:
        fp.seek(0)
    except Exception:
        pass
    return data


def _extract_rows(fields, raw_rows):
    rows = []
    for row in raw_rows:
        if len(rows) >= MAX_SIZE:
            break
        rows.append(dict(zip(fields, row)))
    return rows


def parse_xls(wb, sheets):
    for sheet in wb.sheets():
        if getattr(sheet, 'nrows', None) is None or getattr(sheet, 'ncols', None) is None:
            raise CorruptedError

        ncols = sheet.ncols
        max_cols = min(ncols, MAX_SIZE)
        fields = fix_headers(sheet.row_values(0)[:max_cols])
        raw_rows = (
            row_vals(sheet.row(r)[:max_cols], wb.datemode)
            for r in range(1, sheet.nrows)
        )
        rows = _extract_rows(fields, raw_rows)
        sheets[sheet.name] = (header_population(fields), rows)
    return sheets


def parse_xlsx(wb, sheets):
    for name in wb.sheetnames:
        ws = wb[name]

        if getattr(ws, 'max_row', None) is None or getattr(ws, 'max_column', None) is None:
            raise CorruptedError

        ncols = getattr(ws, "max_column", 0)
        max_cols = min(ncols, MAX_SIZE)
        header_row = next(ws.iter_rows(max_row=1, values_only=True), [])
        fields = fix_headers(list(header_row)[:max_cols])
        raw_rows = (
            row[:max_cols] if row else []
            for row in ws.iter_rows(min_row=2, values_only=True)
        )
        rows = _extract_rows(fields, raw_rows)
        sheets[name] = (header_population(fields), rows)
    return sheets


def fix_headers(raw):
    return [str(v) if v not in (None, '') else f'Unnamed: {i + 1}' for i, v in enumerate(raw)]


def row_vals(row, datemode):
    out = []
    for c in row:
        if c.ctype == xlrd.XL_CELL_DATE:
            out.append(xlrd.xldate.xldate_as_datetime(c.value, datemode).isoformat())
        else:
            out.append(c.value)
    return out
