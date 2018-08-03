import os
from urllib import parse

from furl import furl
from mako.lookup import TemplateLookup

from mfr.core.extension import BaseRenderer
from mfr.extensions.office365.settings import OFFICE_BASE_URL


class Office365Renderer(BaseRenderer):
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
        download_url = furl(self.metadata.download_url).set(query='').url
        return self.TEMPLATE.render(
            base=self.assets_url,
            url=OFFICE_BASE_URL + parse.quote(download_url)
        )

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
