import os
import json
import csv

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
        with open(self.file_path, errors='replace') as fp:
            sheets, size = self._render_grid(fp, self.metadata.ext)
            return self.TEMPLATE.render(
                base=self.assets_url,
                width=settings.TABLE_WIDTH,
                height=settings.TABLE_HEIGHT,
                sheets=json.dumps(sheets),
                options=json.dumps(size),
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
        self._renderer_tabular_metrics = {}

        sheets = self._populate_data(fp, ext)

        size = settings.SMALL_TABLE
        self._renderer_tabular_metrics['size'] = 'small'
        self._renderer_tabular_metrics['nbr_sheets'] = len(sheets)
        for sheet in sheets:
            sheet = sheets[sheet]  # Sheets are stored in key-value pairs of the form {sheet: (col, row)}
            if len(sheet[0]) > 9:  # Check the number of columns
                size = settings.BIG_TABLE
                self._renderer_tabular_metrics['size'] = 'big'

            if len(sheet[0]) > settings.MAX_SIZE or len(sheet[1]) > settings.MAX_SIZE:
                raise exceptions.TableTooBigError('Table is too large to render.', extension=ext)

        return sheets, size

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
                self._renderer_tabular_metrics['importer'] = function.__name__
                try:
                    return imported(fp)
                except KeyError:
                    raise exceptions.UnexpectedFormattingError(
                        'Unexpected formatting error.',
                        extension=self.metadata.ext,
                        formatting_function=str(function),
                    )

        # this will only occur if function_preference is an empty set
        # or all functions in the set raise an import error
        raise exceptions.MissingRequirementsError(
            'Renderer requirements are not met',
            extension=self.metadata.ext,
            function_preference=function_preference,
        )
