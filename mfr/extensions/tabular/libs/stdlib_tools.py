import re
import csv
import logging

from mfr.extensions.tabular import utilities
from mfr.extensions.tabular.settings import MAX_FILE_SIZE, INIT_SNIFF_SIZE
from mfr.extensions.tabular.exceptions import EmptyTableError, TabularRendererError

logger = logging.getLogger(__name__)


def csv_stdlib(fp):
    """Read and convert a csv file to JSON format using the python standard library

    Quirk: ``csv.Sniffer().sniff()`` needs the FULL first row and ONLY one full row to be able to
    effectively detect the correct dialect of the file.

    :param fp: the file pointer object
    :return: a tuple of table headers and data
    """

    # Prepare the first row for sniffing
    data = fp.read(INIT_SNIFF_SIZE)
    data = _trim_or_append_data(fp, data, INIT_SNIFF_SIZE, 0)

    # Reset the file pointer
    fp.seek(0)

    # Sniff the first row to find a matching format
    try:
        dialect = csv.Sniffer().sniff(data)
    except csv.Error:
        dialect = csv.excel
    else:
        _set_dialect_quote_attrs(dialect, data)

    # Explicitly delete data when it is on longer used.
    del data

    # Create the CSV reader with the detected dialect
    reader = csv.DictReader(fp, dialect=dialect)

    # Update the reader field names to avoid duplicate column names when performing row extraction
    columns = []
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

    try:
        rows = [row for row in reader]
    except csv.Error as e:
        if any("field larger than field limit" in errorMsg for errorMsg in e.args):
            raise TabularRendererError(
                'This file contains a field too large to render. '
                'Please download and view it locally.',
                code=400,
                extension='csv',
            ) from e
        else:
            raise TabularRendererError('csv.Error: {}'.format(e), extension='csv') from e

    if not columns and not rows:
        raise EmptyTableError('Table empty or corrupt.', extension='csv')

    del reader
    return {'Sheet 1': (columns, rows)}


def sav_stdlib(fp):
    """Read and convert a .sav file to .csv with pspp, then convert that to JSON format using
    the python standard library

    :param fp: File pointer object to a .sav file
    :return: tuple of table headers and data
    """
    csv_file = utilities.sav_to_csv(fp)
    with open(csv_file.name, 'r') as file:
        csv_file.close()
        return csv_stdlib(file)


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


def _trim_or_append_data(fp, text, read_size, size_to_sniff, max_render_size=MAX_FILE_SIZE):
    """Recursively read data from a file and return its full first row.  The file starts with
    ``text`` and the file pointer points to the next character immediately after `text`.

    :param fp: the file pointer from which data is read
    :param text: the current text chunk to check the new line character
    :param read_size: the last read size when `fp.read()` is called
    :param size_to_sniff: the accumulated size fo the text to sniff
    :param max_render_size: the max file size for render
    :return: the first row of the file in string
    """

    # Return on empty text. This handles the corner case where the CSV is empty or only contains
    # one line without any new line characters.
    if len(text) == 0:
        return ''

    # Try to find the first new line character in the text chunk
    index = _find_new_line(text)
    # If found, return the trimmed substring
    if index != -1:
        return text[:index]
    # Otherwise, update `sniff_size` and then sniff more (2 times of the last `read_size`) text
    size_to_sniff += read_size
    read_size *= 2
    more_text = fp.read(read_size)

    # If text to sniff now goes over the max file size limit, raise the renderer error since there
    # is no need to sniff when the file is already too large to be rendered.
    if size_to_sniff + len(more_text) >= max_render_size:
        raise TabularRendererError(
            'The first row of this file is too large for the sniffer to detect the dialect. '
            'Please download and view it locally.',
            code=400,
            extension='csv'
        )
    # If the size is still within the limit, recursively check `more_text`
    return text + _trim_or_append_data(fp, more_text, read_size, size_to_sniff,
                                       max_render_size=max_render_size)


def _find_new_line(text):
    """In the given text string, find the index of the first occurrence of any of the three types
    of new line character. Note: '\n\r' is not a new line character but two, one LF and one CR.

    1. \r\n     Carriage Return (CR) and Line Feed (LF), must be checked first
    2. \n       LF
    3. \r       CR

    :param text: the text string to check
    :return: the index of the first new line character if found. Otherwise, return -1.
    """
    index = text.find('\r\n')
    if index == -1:
        index = text.find('\n')
        if index == -1:
            index = text.find('\r')
    return index
