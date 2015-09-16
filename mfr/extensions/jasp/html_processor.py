
from io import StringIO
from html.parser import HTMLParser

import base64

class HTMLProcessor(HTMLParser):

    # The HTMLProcessor replaces the src attribute in <image> tags with the base64 equivalent
    # The image content comes from the zip_file (specified with set_src_source())
    # It also strips <script> and <object> tags from the HTML (potential attack vectors)

    html = StringIO()  # buffer for the processed HTML
    zip_file = None

    def set_src_source(self, zip_file):
        self.zip_file = zip_file

    def handle_starttag(self, tag, attrs):
        if tag == 'script' or tag == 'object':  # filter scripts and objects (attack vectors)
            return

        self.html.write('<')
        self.html.write(tag)

        for attr in attrs:
            self.html.write(' ')
            self.html.write(attr[0])
            if attr[1] is not None:
                self.html.write('="')
                if attr[0] == 'src':
                    self._insert_data_uri(attr[1])
                else:
                    self.html.write(attr[1])

                self.html.write('"')

        self.html.write('>')

    def _insert_data_uri(self, src):
        if self.zip_file is None:
            return

        with self.zip_file.open(src) as src_file:
            src_data = src_file.read()
            src_b64 = base64.b64encode(src_data)

            self.html.write('data:image/png;base64,')
            self.html.write(src_b64.decode('utf-8'))

    def handle_endtag(self, tag):
        if tag == 'script' or tag == 'object':
            return

        self.html.write('</')
        self.html.write(tag)
        self.html.write('>')

    def handle_data(self, data):
        self.html.write(data)

    def final_html(self):
        return self.html.getvalue()
