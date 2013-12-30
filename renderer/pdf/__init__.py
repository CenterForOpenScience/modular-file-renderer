from .. import FileRenderer
import os
import PyPDF2


class PdfRenderer(FileRenderer):

    # Gets here using the .pdf extension check then attempts to read the file
        # using pydf2, if it can it accepts it as a valid pdf

    def detect(self, file_pointer):
        if file_pointer.name.endswith('.pdf'):
            try:
                PyPDF2.PdfFileReader(file_pointer)
            except:
                return False
            return True
        return False

    def render(self, file_pointer, file_path):
        pdf = PyPDF2.PdfFileReader(file_pointer)
        
        numPages = pdf.getNumPages()
        html_from_file = open(
            os.getcwd() + "/renderer/pdf/static/html/pdf.html").read()
        html_with_data = '''
            <script>
            var numPages = parseInt({});
            var url = "{}";
            </script>
        '''.format(numPages, file_path) + html_from_file
        return html_with_data
