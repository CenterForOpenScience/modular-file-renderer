import os

import nptdms
from nptdms import TdmsFile
from mako.lookup import TemplateLookup

from mfr.core import extension

# class EscapeHtml(Extension):
#    def extendMarkdown(self, md, md_globals):
#        del md.preprocessors['html_block']
#        del md.inlinePatterns['html']


class TdmsRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics.add('nptdms_version', nptdms.version.__version__)

    def render(self):
        """Render a tdms file to html."""

        tdms_file = TdmsFile.open(self.file_path, raw_timestamps=True)

        body = "<div><ul>"
        for property, value in tdms_file.properties.items():
            body += "<li><b>File</b> = " + str(value) + "</li>\n\n"
        body += "</ul></div><div><ul>"
        for group in tdms_file.groups():
            body += "<li><b>Channel group</b> = " + group.name + "</li>\n"
            body += "<ul>"
            for channel in group.channels():
                body += "<li><b>Channel</b> = " + channel.name + "</li>\n"
                body += "<ul>"
                # Access dictionary of properties:
                for property, value in channel.properties.items():
                    body += "<li>" + property + " = " + str(value) + "</li>\n\n"

                # Access numpy array of data for channel:
                # body = body + str(channel[:]) + ""
                body += "</ul>"
            body += "</ul>"
        body += "</ul></div>"

        return self.TEMPLATE.render(base=self.assets_url, body=body)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
