import re

from mfr.extensions.tabular import compat


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
