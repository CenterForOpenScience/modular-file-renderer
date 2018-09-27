import os

from mako.lookup import TemplateLookup
from mfr.core import extension
from mfr.extensions.utils import munge_url_for_localdev

from mfr.extensions.codepygments import CodePygmentsRenderer
from mfr.extensions.image import ImageRenderer
from mfr.extensions.unoconv import UnoconvRenderer
from mfr.extensions.tabular import TabularRenderer


RENDERERS = {
    'application/vnd.google-apps.spreadsheet': TabularRenderer,
    'application/vnd.google-apps.document': UnoconvRenderer,
    'application/vnd.google-apps.drawing': ImageRenderer,
    'application/vnd.google-apps.presentation': UnoconvRenderer
}
class DefaultRenderer(extension.BaseRenderer):
    """Default renderer. used when the file we're trying to render has no
    extension. This will apply to plain text files and google drive
    documents.
    """

    def __new__(self, metadata, path, url, assets_url, export_url):
        try:
            return RENDERERS[metadata.content_type](metadata, path, url, assets_url, export_url)
        except:
            return CodePygmentsRenderer(metadata, path, url, assets_url, export_url)
