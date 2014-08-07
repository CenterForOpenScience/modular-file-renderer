# import pandas
import csv
from mfr.core import RenderResult
# import json
from mako.lookup import TemplateLookup

template = TemplateLookup(
    directories=['mfr_tabular/templates']
).get_template('tabular.mako')


def column_population(fields):
    """make column headers from the keys in dataframe
    :param dataframe:
    :return: a list of dictionaries
    """
    columns = []
    for field in fields:
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


def render_html(fp, src=None):

    with open(fp.name) as infile:
        dialect = csv.Sniffer().sniff(infile.read(1024))
        infile.seek(0)
        has_header = csv.Sniffer().has_header(infile.read())
        infile.seek(0)
        reader = csv.reader(infile, dialect)
        data = [row for row in reader]

    header = []
    if has_header:
        print "yessss"
        header = data[0]
        data = data[1:]

    # dataframe = pandas.read_csv(fp.name)
    print "header", header
    print "data", data

    columns = column_population(header)
    rows = row_population(data, fields=header)

    print "columns", columns
    print "rows", rows

    content = template.render(
        columns=columns,
        rows=rows,
        writing='yes',
        STATIC_PATH="/mfr/mfr_tabular",
    )

    return RenderResult(content=content)
