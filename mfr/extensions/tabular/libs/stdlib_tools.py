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
    columns = [
        {
            'id': fieldname,
            'field': fieldname,
            'name': fieldname,
        }
        for fieldname in reader.fieldnames
    ]
    rows = [row for row in reader]
    return columns, rows
