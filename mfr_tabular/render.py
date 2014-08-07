from mfr.core import RenderResult
from mako.lookup import TemplateLookup

try:
    import pandas
    PANDAS = True
except IOError:
    PANDAS = False
    import csv
template = TemplateLookup(
    directories=['mfr_tabular/templates']
).get_template('tabular.mako')


def column_population(data):
    """make column headers from the keys in dataframe
    :param dataframe:
    :return: a list of dictionaries
    """
    columns = []
    for field in data:
        columns.append({
            'id': field,
            'name': field,
            'field': field,
        })
    return columns


def row_population(data, fields=None):
    """Convert the dictionary of lists Pandas has generated from the CSV into
    a list of dicts.
    :param dataframe:
    :return: JSON representation of rows
    """
    # todo this needs to be reformatted NOT to use the row names as a variable
    # to iterate over, this will break spss
    # files that need rownames
    # todo right now it is renaming the rows in [r] when it reads it in
    if not fields:
        fields = data[0]

    rows = []
    for n in range(len(data)):
        rows.append({})
        for i in range(len(fields)):
            rows[n][fields[i]] = str(data[n][i])
    return rows


def pandas_row_pop(dataframe):
    fields = dataframe.keys()
    rows = []
    for n in range(len(dataframe[fields[0]])):
        rows.append({})
        for col_fields in fields:
            rows[n][col_fields] = str(dataframe[col_fields][n])

    return rows


def data_from_csv(fp):

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

    dataframe = pandas.read_csv(fp.name)
    fields = dataframe.keys()
    columns = column_population(fields)
    rows = pandas_row_pop(dataframe)

    return columns, rows


def render_html(fp, src=None):

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
