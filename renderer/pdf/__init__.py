from .. import FileRenderer

class PdfRenderer(FileRenderer):

    def detect(self, fp):
        return fp.name.endswith('pdf')

    def render(self, fp, path):
        return '''

            <!-- Include PDF.JS -->
            <script type="text/javascript src="/static/pdf/js/pdf.js"></script>
            <script type="text/javascript src="/static/pdf/js/???"></script>

            <script type="text/javascript">
                var pdf = PDFJS.getDocument('{url}');
                pdf.then(renderPage);
            </script>

            <div id="pdfContainer"></div>
        '''.format(
            url='path/to/pdf'
        )
