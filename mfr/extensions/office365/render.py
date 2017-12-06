import os
from urllib import parse

import furl
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.office365 import settings as office365_settings


class Office365Renderer(extension.BaseRenderer):
    """A renderer for .docx files that are publicly available.

    Office online can render `.docx` files to `.pdf` for us. This renderer will only be made
    if a query param with `public_file=true` is present. It then generates and embeds an
    office online URL into an `iframe` and returns the template. The file it is trying to
    render MUST be public.

    Note: this renderer DOES NOT work locally.

    """

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        download_url = furl.furl(self.metadata.download_url).set(query='').url
        encoded_download_url = parse.quote(download_url)
        office_render_url = office365_settings.OFFICE_BASE_URL + encoded_download_url
        return self.TEMPLATE.render(base=self.assets_url, url=office_render_url)

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
