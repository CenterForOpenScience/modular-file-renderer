import os
import json

from mako.lookup import TemplateLookup
from mfr.core import extension

from mfr.extensions.tabular import settings
from mfr.extensions.tabular import exceptions


class TabularRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        with open(self.file_path) as fp:
            columns, rows = self._render_grid(fp, self.extension)
            return self.TEMPLATE.render(
                base=self.assets_url,
                width=settings.TABLE_WIDTH,
                height=settings.TABLE_HEIGHT,
                columns=json.dumps(columns),
                rows=json.dumps(rows),
                options=json.dumps(settings.SMALL_TABLE if len(columns) < 9 else settings.BIG_TABLE),
            )

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True

    def _render_grid(self, fp, ext, *args, **kwargs):  # assets_path, ext):
        """Render a tabular file to html
        :param fp: file pointer object
        :return: RenderResult object containing html and assets
        """
        columns, rows = self._populate_data(fp, ext)

        if len(columns) > settings.MAX_SIZE or len(rows) > settings.MAX_SIZE:
            raise exceptions.TableTooBigException("Table is too large to render.", code=400)

        if len(columns) < 1 or len(rows) < 1:
            raise exceptions.EmptyTableException("Table is empty or corrupt.", code=400)

        return columns, rows

    def _populate_data(self, fp, ext):
        """Determine the appropriate library and use it to populate rows and columns
        :param fp: file pointer
        :param ext: file extension
        :return: tuple of column headers and row data
        """
        function_preference = settings.LIBS.get(ext)

        for function in function_preference:
            try:
                imported = function()
            except ImportError:
                pass
            else:
                try:
                    return imported(fp)
                except KeyError:
                    raise exceptions.UnexpectedFormattingException()

        raise exceptions.MissingRequirementsException('Renderer requirements are not met')
