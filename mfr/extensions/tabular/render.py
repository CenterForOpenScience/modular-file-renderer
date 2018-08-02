import json
import gc
import logging
import os

from humanfriendly import format_size
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.tabular import settings, exceptions

logger = logging.getLogger(__name__)


class TabularRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        file_size = os.path.getsize(self.file_path)
        if file_size > settings.MAX_FILE_SIZE:
            raise exceptions.FileTooLargeError(
                'Tabular files larger than {} are not rendered. Please download '
                'the file to view.'.format(format_size(settings.MAX_FILE_SIZE, binary=True)),
                file_size=file_size,
                max_size=settings.MAX_FILE_SIZE,
                extension=self.metadata.ext,
            )

        with open(self.file_path, errors='replace') as fp:
            sheets, size, nbr_rows, nbr_cols = self._render_grid(fp, self.metadata.ext)

        # Force GC
        gc.collect()

        if sheets and size:
            return self.TEMPLATE.render(
                base=self.assets_url,
                width=settings.TABLE_WIDTH,
                height=settings.TABLE_HEIGHT,
                sheets=json.dumps(sheets),
                options=json.dumps(size),
            )

        assert nbr_rows and nbr_cols
        raise exceptions.TableTooBigError(
            'Table is too large to render.',
            extension=self.metadata.ext,
            nbr_cols=nbr_cols,
            nbr_rows=nbr_rows
        )

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True

    def _render_grid(self, fp, ext, *args, **kwargs):
        """Render a tabular file to html
        :param fp: file pointer object
        :return: RenderResult object containing html and assets
        """
        self._renderer_tabular_metrics = {}

        sheets = self._populate_data(fp, ext)

        size = settings.SMALL_TABLE
        self._renderer_tabular_metrics['size'] = 'small'
        self._renderer_tabular_metrics['nbr_sheets'] = len(sheets)

        table_too_big = False
        nbr_cols = 0
        nbr_rows = 0

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
                table_too_big = True
                break

        if table_too_big:
            del sheets
            return None, None, nbr_rows, nbr_cols

        return sheets, size, None, None

    def _populate_data(self, fp, ext):
        """Determine the appropriate library and use it to populate rows and columns
        :param fp: file pointer
        :param ext: file extension
        :return: a dict mapping sheet titles to tuples of column headers and row data
        """
        function_preference = settings.LIBS.get(ext.lower())

        for populate_func in function_preference:
            try:
                imported = populate_func()
            except ImportError:
                pass
            else:
                self._renderer_tabular_metrics['importer'] = populate_func.__name__
                try:
                    return imported(fp)
                except (KeyError, ValueError) as err:
                    logger.error('WB has encountered an unexpected error '
                                 'when trying to render a tabular file: {}'.format(err))
                    raise exceptions.UnexpectedFormattingError(
                        'Unexpected formatting error.',
                        extension=self.metadata.ext,
                        formatting_function=str(populate_func),
                    )

        # this will only occur if function_preference is an empty set
        # or all functions in the set raise an import error
        raise exceptions.MissingRequirementsError(
            'Renderer requirements are not met',
            extension=self.metadata.ext,
            function_preference=function_preference,
        )
