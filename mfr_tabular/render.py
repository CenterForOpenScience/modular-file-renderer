import json
import os
from mfr.core import RenderResult, get_file_extension
from mako.template import Template
from .configuration import config


def render_html(fp, src=None):
    """Render a tabular file to html
    :param fp: file pointer object
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
        return RenderResult("Table is empty")

    template = Template(filename='mfr_tabular/templates/tabular.mako')

    content = template.render(
        columns=json.dumps(columns),
        rows=json.dumps(rows),
        # TODO(asmacdo) make this a title?
        writing="",
    )

    assets = {
        'css': find_assets('css'),
        'js': find_assets('js')
    }

    return RenderResult(content=content, assets=assets)


def find_assets(asset_type):
    """Create dictionary of js and css assets"""

    static_dir = "/static/mfr/mfr_tabular"
    files = os.listdir("mfr_tabular/static/{asset}".format(asset=asset_type))

    return ['{0}/{1}/{2}'.format(static_dir, asset_type, filename)
            for filename in files]


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
