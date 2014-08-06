import pandas
from mfr.core import RenderResult, collect_static
import json
from mako.lookup import TemplateLookup

template = TemplateLookup(
    directories=['mfr_tabular/templates']
).get_template('tabular.mako')


def column_population(dataframe):
    """make column headers from the keys in dataframe
    :param dataframe:
    :return: a list of dictionaries
    """
    fields = dataframe.keys()

    columns = []
    for field in fields:
        uni = field
        columns.append({
            'id': uni,
            'name': uni,
            'field': uni,
        })
    return columns


def row_population(dataframe):
    """Convert the dictionary of lists Pandas has generated from the CSV into
    a list of dicts.
    :param dataframe:
    :return: JSON representation of rows
    """
    # todo this needs to be reformatted NOT to use the row names as a variable
    # to iterate over, this will break spss
    # files that need rownames
    # todo right now it is renaming the rows in [r] when it reads it in
    fields = dataframe.keys()
    rows = []
    for n in range(len(dataframe[fields[0]])):
        rows.append({})
        for col_field in fields:
            rows[n][col_field] = str(dataframe[col_field][n])
    return rows


def render_html(fp, src=None):

    dataframe = pandas.read_csv(fp.name)

    columns = json.dumps(column_population(dataframe), sort_keys=True, indent=4)
    rows = json.dumps(row_population(dataframe), sort_keys=True, indent=4)

    print columns
    print rows

    collect_static()

    content = template.render(
        columns=columns,
        rows=rows,
        writing='',
        STATIC_PATH="path",
    )

    print content

    return RenderResult(content=content)
