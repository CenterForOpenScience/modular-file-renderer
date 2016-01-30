import csv
import re
from ..exceptions import EmptyTableException


def csv_stdlib(fp):
    """Read and convert a csv file to JSON format using the python standard library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    data = fp.read(2048)
    fp.seek(0)

    try:
        dialect = csv.Sniffer().sniff(data)
    except csv.Error:
        dialect = csv.excel
    else:
        _set_dialect_quote_attrs(dialect, data)

    reader = csv.DictReader(fp, dialect=dialect)
    columns = []
    # update the reader field names to avoid duplicate column names when performing row extraction
    for idx, fieldname in enumerate(reader.fieldnames or []):
        column_count = sum(1 for column in columns if fieldname == column['name'])
        if column_count:
            unique_fieldname = '{}-{}'.format(fieldname, column_count + 1)
            reader.fieldnames[idx] = unique_fieldname
        else:
            unique_fieldname = fieldname
        columns.append({
            'id': unique_fieldname,
            'field': unique_fieldname,
            'name': fieldname,
            'sortable': True,
        })
    rows = [row for row in reader]

    if not columns and not rows:
        raise EmptyTableException("Table empty or corrupt.")

    return {'Sheet 1': (columns, rows)}


def _set_dialect_quote_attrs(dialect, data):
    """Set quote-related dialect attributes based on up to 2kb of csv data.

    The regular expressions search for things that look like the beginning of
    a list, wrapped in a quotation mark that is not dialect.quotechar, with
    list items wrapped in dialect.quotechar and seperated by commas.

    Example matches include:
        "['1', '2', '3'         for quotechar == '
        '{"a", "b", "c"         for quotechar == "
    """
    if dialect.quotechar == '"':
        if re.search('\'[[({]".+",', data):
            dialect.quotechar = "'"
        if re.search("'''[[({]\".+\",", data):
            dialect.doublequote = True
    elif dialect.quotechar == "'":
        if re.search("\"[[({]'.+',", data):
            dialect.quotechar = '"'
        if re.search('"""[[({]\'.+\',', data):
            dialect.doublequote = True
