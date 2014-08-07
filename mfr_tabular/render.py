from mfr.core import RenderResult, get_file_extension
from mako.lookup import TemplateLookup
from dependencies import pandas
from utilities import column_population, row_population
from panda_tools import data_from_pandas
from csv_tools import data_from_csv

template = TemplateLookup(
    directories=['mfr_tabular/templates']
).get_template('tabular.mako')


def render_html(fp, src=None):
    """Determine which library to use and render a csv to html
    :param fp: file pointer object
    :param src:
    :return: RenderResult object containing html and assets
    """
    ext = get_file_extension(fp.name)

    if pandas and not ext == '.tsv':
        columns, rows = data_from_pandas(fp)
    else:
        columns, rows = data_from_csv(fp)

    content = template.render(
        columns=columns,
        rows=rows,
        writing="Pandas = " + str(pandas and not ext == '.tsv'),
        STATIC_PATH="/mfr/mfr_tabular",
    )

    return RenderResult(content=content)
