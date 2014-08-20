import json
import os
import mfr
from .exceptions import TableTooBigException, EmptyTableException, MissingRequirementsException
from mfr.core import RenderResult, get_file_extension
from mako.template import Template
from .configuration import config


def render_html(fp, src=None):
    """Render a tabular file to html
    :param fp: file pointer object
    :return: RenderResult object containing html and assets
    """

    columns, rows = populate_data(fp)

    max_size = config.get('max_size')

    if len(columns) > max_size or len(rows) > max_size:
        raise TableTooBigException

    if len(columns) < 1 or len(rows) < 1:
        raise EmptyTableException

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

    assets_uri_base = '{0}/mfr_tabular'.format(mfr.config['STATIC_URL'])
    static_path = os.path.abspath(os.path.join("mfr_tabular", "static", asset_type))

    return ['{0}/{1}/{2}'.format(assets_uri_base, asset_type, filepath)
            for filepath in os.listdir(static_path)]


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

    raise MissingRequirementsException('Renderer requirements are not met')
