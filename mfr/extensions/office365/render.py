import os
import furl

from mfr.core import extension
from mako.lookup import TemplateLookup
from mfr.extensions.office365 import settings


class Office365Renderer(extension.BaseRenderer):
    """A renderer for use with public .docx files.

    Office online can render .docx files to pdf for us.
    This renderer will only ever be made if a query param with `public_file=1` is sent.
    It then generates and embeds an office online url into an
    iframe and returns the template. The file it is trying to render MUST
    be available publically online. This renderer will not work if testing locally.

    """

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        download_url = furl.furl(self.metadata.download_url).set(query='')
        url = settings.OFFICE_BASE_URL + download_url.url
        return self.TEMPLATE.render(base=self.assets_url, url=url)

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
