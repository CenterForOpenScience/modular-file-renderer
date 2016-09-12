import re
import subprocess
from tempfile import NamedTemporaryFile

from mfr.core import exceptions
from mfr.extensions.tabular import compat, settings


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
        subprocess.check_call([
            settings.PSPP_CONVERT_BIN,
            fp.name,
            csv_file.name,
        ])
    except subprocess.CalledProcessError:
        raise exceptions.ExporterError(
            'Unable to convert the SPSS file to CSV, please try again later.', code=400)
    return csv_file
