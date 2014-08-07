from mfr.core import RenderResult
from mako.lookup import TemplateLookup
import csv

try:
    import pandas
    PANDAS = True
except IOError:
    PANDAS = False

template = TemplateLookup(
    directories=['mfr_tabular/templates']
).get_template('tabular.mako')


def column_population(headers):
    """make column headers from a list
    :param headers: list of column headers
    :return: a list of dictionaries
    """
    columns = []
    for field in headers:
        columns.append({
            'id': field,
            'name': field,
            'field': field,
        })
    return columns


def row_population(data, fields=None):
    """Convert a list of lists into a list of dicts associating each
    cell with its column header and row
    :param data: two dimensional list of data
    :param fields: column headers
    :return: JSON representation of rows
    """

    if not fields:
        fields = data[0]

    rows = []
    for n in range(len(data)):
        rows.append({})
        for i in range(len(fields)):
            rows[n][fields[i]] = str(data[n][i])
    return rows


def pandas_row_population(dataframe):
    """Convert dataframe into JSON repr of rows
    :param dataframe: object containing data
    :return: rows of data in JSON format
    """

    fields = dataframe.keys()
    rows = []
    for n in range(len(dataframe[fields[0]])):
        rows.append({})
        for col_fields in fields:
            rows[n][col_fields] = str(dataframe[col_fields][n])

    return rows


def data_from_csv(fp):
    """Read and convert a csv file to JSON format using the csv library
    :param fp: File pointer object
    :return: tuple of columns and rows
    """

    with open(fp.name) as infile:
        dialect = csv.Sniffer().sniff(infile.read(1024))
        infile.seek(0)
        # TODO(asmacdo) Nice way of displaying if there is no header
        # has_header = csv.Sniffer().has_header(infile.read())
        # infile.seek(0)
        reader = csv.reader(infile, dialect)
        data = [row for row in reader]

    columns = column_population(data[0])
    rows = row_population(data[1:], data[0])

    return columns, rows


def data_from_pandas(fp):
    """Read and convert a csv to JSON format using the pandas library
    :param fp: File pointer object
    :return: tuple of columns and rows
    """

    dataframe = pandas.read_csv(fp.name)
    fields = dataframe.keys()
    columns = column_population(fields)
    rows = pandas_row_population(dataframe)

    return columns, rows


def render_html(fp, src=None):
    """Determine which library to use and render a csv to html
    :param fp: file pointer object
    :param src:
    :return: RenderResult object containing html and assets
    """

    PANDAS = False

    if PANDAS:
        columns, rows = data_from_pandas(fp)
    else:
        columns, rows = data_from_csv(fp)

    content = template.render(
        columns=columns,
        rows=rows,
        writing="Pandas = " + str(PANDAS),
        STATIC_PATH="/mfr/mfr_tabular",
    )

    return RenderResult(content=content)
