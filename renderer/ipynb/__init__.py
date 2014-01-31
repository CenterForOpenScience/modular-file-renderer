from .. import FileRenderer
from flask import render_template

from IPython.config import Config
from IPython.nbconvert import export_python
from IPython.nbconvert.exporters import HTMLExporter
from IPython.nbformat import current as nbformat

c = Config()
c.HTMLExporter.template_file = 'basic'
c.NbconvertApp.fileext = 'html'
c.CSSHTMLHeaderTransformer.enabled = False
c.Exporter.filters = {'strip_files_prefix': lambda s: s} #don't strip the files prefix
exporter = HTMLExporter(config=c)

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
        name, theme = self._get_metadata(nb)
        body = exporter.from_notebook_node(nb)[0] 
        context =  {'file_name': name,
                    'css_theme': theme, #'css_linalg', 'cdp_1'
                    'mathjax_conf': None,
                    'body': body }
        return render_template('ipynb/notebook.html', **context)

    def export_ipynb(self, fp):
        return fp.read(), '.ipynb'

    def export_python(self, fp):
        output, resources = export_python(fp)
        return output, '.py'

    def _parse_json(self, content):
        try :
            nb = nbformat.reads_json(content)
        except ValueError:
            raise NbFormatError('Error reading json notebook')
        return nb

    def _get_metadata(self, nb):
        # notebook title
        name = nb.get('metadata', {})\
                 .get('name', None) 
        if not name:
            name = "untitled.ipynb"
        if not name.endswith(".ipynb"):
            name = name + ".ipynb"

        # css
        css_theme = nb.get('metadata', {})\
                      .get('_nbviewer', {})\
                      .get('css', None)
        if css_theme and not re.match('\w', css_theme):
            css_theme = None

        return name, css_theme   

