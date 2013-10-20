from .. import FileRenderer

from flask import render_template
from IPython.nbformat import current as nbformat
from IPython.nbconvert.exporters import HTMLExporter
from IPython.config import Config

# Instantiate and configure the exporter
config = Config()
config.HTMLExporter.template_file = 'basic'
config.NbconvertApp.fileext = 'html'
config.CSSHTMLHeaderTransformer.enabled = False
# don't strip the files prefix - we use it for redirects
config.Exporter.filters = {'strip_files_prefix': lambda s: s}

html_exporter = HTMLExporter(config=config)

class NbFormatError(Exception):
    pass

class IPynbRenderer(FileRenderer):
    def detect(self, fp):
        fname = fp.name
        for ext in ['ipynb', 'json']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        content = fp.read()
        nb = self._parse_json(content)
        name, css_theme = self._get_metadata(nb)
        body = html_exporter.from_notebook_node(nb)[0] 
        context =  {'download_url': None,
                    'download_name': name,
                    'css_theme': css_theme,
                    'mathjax_conf': None,
                    'body': body }
        # render template
        return render_template('notebook.html', **context)

    def _parse_json(self, content):
        try :
            nb = nbformat.reads_json(content)
        except ValueError:
            raise NbFormatError('Error reading json notebook')
        return nb

    def _get_metadata(self, nb):
        # css
        css_theme = nb.get('metadata', {})\
                      .get('_nbviewer', {})\
                      .get('css', None)
        if css_theme and not re.match('\w', css_theme):
            css_theme = None

        # get the notebook title
        try:
            name = nb.metadata.name
        except AttributeError:
            name = None  
        if not name:
            name = url.rsplit('/')[-1]
        if not name.endswith(".ipynb"):
            name = name + ".ipynb"

        return name, css_theme   


