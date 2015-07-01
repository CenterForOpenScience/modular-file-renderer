import csv


def csv_stdlib(fp):
    """Read and convert a csv file to JSON format using the python standard library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    try:
        dialect = csv.Sniffer().sniff(fp.read(2048))
    except csv.Error:
        dialect = csv.excel

    fp.seek(0)
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
    return columns, rows
