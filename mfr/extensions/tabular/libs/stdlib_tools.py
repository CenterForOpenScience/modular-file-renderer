import csv
from http import HTTPStatus

from mfr.extensions.tabular import utilities
from mfr.extensions.tabular.exceptions import (EmptyTableError,
                                               TabularRendererError)


def csv_stdlib(fp):
    try:
        # CSVs are always values seperated by commas
        # sniff for quoting, and spaces after commas
        dialect = csv.Sniffer().sniff(fp.read(), ',')
    except:
        dialect = csv.excel
    fp.seek(0)

    reader = csv.DictReader(fp, dialect=dialect)
    return parse_stdlib(reader, 'csv')

def tsv_stdlib(fp):
    try:
        # TSVs are always values seperated by TABs
        # sniff for quoting, and spaces after TABs
        dialect = csv.Sniffer().sniff(fp.read(), '\t')
    except:
        dialect = csv.excel_tab
    fp.seek(0)

    reader = csv.DictReader(fp, dialect=dialect)
    return parse_stdlib(reader, 'tsv')

def parse_stdlib(reader, ext):
    """Read and convert a csv like file to JSON format using the python standard library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    columns = []
    # update the reader field names to avoid duplicate column names when performing row extraction
    try:
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
    except csv.Error as e:
        if any("field larger than field limit" in errorMsg for errorMsg in e.args):
            raise TabularRendererError(
                'This file contains a field too large to render. '
                'Please download and view it locally.',
                code=HTTPStatus.BAD_REQUEST,
                extension=ext,
            ) from e
        else:
            raise TabularRendererError(
                'Cannot render file as {}. The file may be empty or corrupt'.format(ext),
                code=HTTPStatus.BAD_REQUEST,
                extension=ext
            ) from e

    # Outside other except because the `if any` line causes more errors to be raised
    # on certain exceptions
    except Exception as e:
        raise TabularRendererError(
            'Cannot render file as {}. The file may be empty or corrupt'.format(ext),
            code=HTTPStatus.BAD_REQUEST,
            extension=ext
        ) from e

    if not columns and not rows:
        raise EmptyTableError(
            'Cannot render file as {}. The file may be empty or corrupt'.format(ext),
            code=HTTPStatus.BAD_REQUEST,
            extension=ext)

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
