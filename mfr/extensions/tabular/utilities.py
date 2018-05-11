import re
from http import HTTPStatus
from subprocess import (check_call,
                        TimeoutExpired,
                        CalledProcessError)
from tempfile import NamedTemporaryFile

from mfr.extensions.tabular import compat
from mfr.core.exceptions import SubprocessError
from mfr.extensions.tabular.settings import (PSPP_CONVERT_BIN,
                                             PSPP_CONVERT_TIMEOUT)


def header_population(headers):
    """make column headers from a list
    :param headers: list of column headers
    :return: a list of dictionaries
    """
    return [{'id': field, 'name': field, 'field': field, 'sortable': True} for field in headers]


def data_population(in_data, headers=None):
    """Convert a list of lists into a list of dicts associating each
    cell with its column header and row
    :param data: two dimensional list of data
    :param fields: column headers
    :return: JSON representation of rows
    """
    headers = headers or in_data[0]

    return [
        dict([(header, row[cindex])
            for cindex, header in enumerate(headers)])
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
