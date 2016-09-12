import os

import markdown
from markdown.extensions import Extension

from mako.lookup import TemplateLookup

from mfr.core import extension


class EscapeHtml(Extension):
    def extendMarkdown(self, md, md_globals):
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']


class MdRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics.add('markdown_version', markdown.version)

    def render(self):
        """Render a markdown file to html."""
        with open(self.file_path, 'r') as fp:
            body = markdown.markdown(fp.read(), extensions=[EscapeHtml()])
            return self.TEMPLATE.render(base=self.assets_url, body=body)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
