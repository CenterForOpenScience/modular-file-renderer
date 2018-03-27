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
        for sheet_title in sheets:
            sheet = sheets[sheet_title]

            # sheet is a two-element list.  sheet[0] is a list of dicts containing metadata about
            # the column headers.  Each dict contains four keys: `field`, `name`, `sortable`, `id`.
            # sheet[1] is a list of dicts where each dict contains the row data.  The keys are the
            # fields the data belongs to and the values are the data values.

            nbr_cols = len(sheet[0])
            if nbr_cols > 9:
                size = settings.BIG_TABLE
                self._renderer_tabular_metrics['size'] = 'big'

            nbr_rows = len(sheet[1])
            if nbr_cols > settings.MAX_SIZE or nbr_rows > settings.MAX_SIZE:
                raise exceptions.TableTooBigError('Table is too large to render.', extension=ext,
                                                  nbr_cols=nbr_cols, nbr_rows=nbr_rows)

        return sheets, size

    def _populate_data(self, fp, ext):
        """Determine the appropriate library and use it to populate rows and columns
        :param fp: file pointer
        :param ext: file extension
        :return: a dict mapping sheet titles to tuples of column headers and row data
        """
        function_preference = settings.LIBS.get(ext.lower())

        for function in function_preference:
            try:
                imported = function()
            except ImportError:
                pass
            else:
                self._renderer_tabular_metrics['importer'] = function.__name__
                try:
                    return imported(fp)
                except (KeyError, ValueError):
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
