import os

from mako.lookup import TemplateLookup
from mfr.core import extension
from mfr.extensions.utils import munge_url_for_localdev

from mfr.extensions.image import ImageExporter
from mfr.extensions.unoconv import UnoconvExporter


EXPORTERS = {
    'application/vnd.google-apps.spreadsheet': UnoconvExporter,
    'application/vnd.google-apps.document': UnoconvExporter,
    'application/vnd.google-apps.drawing': ImageExporter,
    'application/vnd.google-apps.presentation': UnoconvExporter
}


class DefaultExporter(extension.BaseExporter):
    """Default renderer. used when the file we're trying to render has no
    extension. This will apply to plain text files and google drive
    documents.
    """

    def __new__(self, normalized_name, source_path, output_path, format, metadata):
        return EXPORTERS[metadata.content_type](normalized_name, source_path, output_path, format, metadata)
