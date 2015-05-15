"""Tabular data renderer module.

.. note::

    jQuery must be included on the page for this renderer to work properly.
"""
import json
import os
from mfr.core import extension
from .configuration import defaults, MAX_SIZE, TABLE_HEIGHT, TABLE_WIDTH
from .exceptions import TableTooBigException, \
    EmptyTableException, MissingRequirementsException, \
    UnexpectedFormattingException

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'templates', 'tabular.html')


def render_html(fp, assets_path, ext):
    """Render a tabular file to html
    :param fp: file pointer object
    :return: RenderResult object containing html and assets
    """
    columns, rows = populate_data(fp, ext)

    max_size = MAX_SIZE
    table_width = TABLE_WIDTH
    table_height = TABLE_HEIGHT

    if len(columns) > max_size or len(rows) > max_size:
        raise TableTooBigException("Table is too large to render.")

    if len(columns) < 1 or len(rows) < 1:
        raise EmptyTableException("Table is empty or corrupt.")

    table_size = 'small_table' if len(columns) < 9 else 'big_table'
    slick_grid_options = defaults.get('slick_grid_options').get(table_size)

    try:
        columns = json.dumps(columns)
        rows = json.dumps(rows)
    except UnicodeDecodeError:
        raise UnexpectedFormattingException()

    with open(TEMPLATE) as template:
        content = template.read().format(
            width=table_width,
            height=table_height,
            columns=columns,
            rows=rows,
            options=json.dumps(slick_grid_options),
            base=assets_path,
        )

    return content


def populate_data(fp, ext):
    """Determine the appropriate library and use it to populate rows and columns
    :param fp: file pointer
    :param ext: file extension
    :return: tuple of column headers and row data
    """
    function_preference = defaults['libs'].get(ext)

    for function in function_preference:
        try:
            imported = function()
        except ImportError:
            pass
        else:
            try:
                return imported(fp)
            except KeyError:
                raise UnexpectedFormattingException()

    raise MissingRequirementsException('Renderer requirements are not met')


class TabularRenderer(extension.BaseRenderer):

    def render(self):
        with open(self.file_path, 'r') as fp:
            return render_html(fp, self.assets_url, self.extension)

    @property
    def requires_file(self):
        return True
