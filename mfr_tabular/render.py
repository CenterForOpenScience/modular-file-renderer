from mfr.core import RenderResult, get_file_extension
from mako.lookup import TemplateLookup
from dependencies import pandas
from panda_tools import data_from_pandas
from csv_tools import data_from_csv
from xlrd_tools import data_from_xlrd

template = TemplateLookup(
    directories=['mfr_tabular/templates']
).get_template('tabular.mako')


def render_html(fp, src=None):
    """Render a tabular file to html
    :param fp: file pointer object
    :param src:
    :return: RenderResult object containing html and assets
    """

    columns, rows = populate_data(fp)

    content = template.render(
        columns=columns,
        rows=rows,
        # TODO(asmacdo) make this a title?
        writing="",
        # TODO(asmacdo) investigate
        STATIC_PATH="/mfr/mfr_tabular",
    )

    assets = get_assets()

    return RenderResult(content=content, assets=assets)


def get_assets():
    static_dir = "/static/mfr/mfr_tabular"

    assets = {}

    css_files = [
        "slick.grid.css",
        "jquery-ui-1.8.16.custom.css",
        "examples.css",
        "slick-default-theme.css",
    ]

    js_files = [
        "jquery-1.7.min.js",
        "jquery.event.drag-2.2.js",
        "slick.core.js",
        "slick.grid.js",
    ]

    css_full_paths = [static_dir + '/css/' + filename for filename in css_files]
    js_full_paths = [static_dir + '/js/' + filename for filename in js_files]

    assets['js'] = js_full_paths
    assets['css'] = css_full_paths

    return assets


def populate_data(fp):
    """Determine the appropriate library and use it to populate rows and columns
    :param fp: file pointer
    :return: tuple of column headers and data
    """
    ext = get_file_extension(fp.name)

    if ext == '.tsv':
        headers, data = data_from_csv(fp)
    elif ext == '.csv':
        if pandas:
            headers, data = data_from_pandas(fp)
    elif ext == '.xls':
        headers, data = data_from_xlrd(fp)


    return headers, data
