from mfr.core import RenderResult, get_file_extension
from mako.lookup import TemplateLookup
import json
from .configuration import config

template = TemplateLookup(
    directories=['mfr_tabular/templates']
).get_template('tabular.mako')


def render_html(fp, src=None):
    """Render a tabular file to html
    :param fp: file pointer object
    :param src:
    :return: RenderResult object containing html and assets
    """

    try:
        columns, rows = populate_data(fp)
    except TypeError:
        return RenderResult("A matching renderer was not found or render "
                            + "requirements are not met")

    max_size = config.get('max_size')

    if len(columns) > max_size or len(rows) > max_size:
        return RenderResult("Table is too large")

    if len(columns) < 1 or len(rows) < 1:
        return RenderResult("Table is invalid")

    content = template.render(
        columns=json.dumps(columns),
        rows=json.dumps(rows),
        # TODO(asmacdo) make this a title?
        writing="",
        # TODO(asmacdo) investigate
        STATIC_PATH="/mfr/mfr_tabular",
    )

    assets = get_assets()

    return RenderResult(content=content, assets=assets)


def get_assets():
    """Create dictionary of js and css assets"""

    static_dir = "/static/mfr/mfr_tabular"

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

    assets = {}
    assets['css'] = [static_dir + '/css/' + filename for filename in css_files]
    assets['js'] = [static_dir + '/js/' + filename for filename in js_files]

    return assets


# TODO(asmacdo) better way of choosing the renderer
def populate_data(fp):
    """Determine the appropriate library and use it to populate rows and columns
    :param fp: file pointer
    :return: tuple of column headers and row data
    """

    ext = get_file_extension(fp.name)
    function_preference = config['tabular_libraries'].get(ext)

    for function in function_preference:
        try:
            imported = function()
            print("Trying " + imported.__name__)
            return imported(fp)
        except ImportError:
            print("Failed to import " + function.__name__)
