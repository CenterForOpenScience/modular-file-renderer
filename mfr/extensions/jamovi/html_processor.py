import base64
from html.parser import HTMLParser
from io import StringIO
from urllib import parse


class HTMLProcessor(HTMLParser):

    # The HTMLProcessor replaces the src attribute in <image> tags with the base64 equivalent.
    # The image content comes from the zip_file (specified with set_src_source()).
    # It also strips <script> and <object> tags and on$foo attributes from the HTML (potential
    # attack vectors)

    FILTERED_TAGS = ['script', 'object']

    def __init__(self, zip_file):
        HTMLParser.__init__(self)
        self._html = StringIO()  # buffer for the processed HTML
        self._zip_file = zip_file

        # used to exclude the contents of script and object tags
        self._excl_nested_level = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.FILTERED_TAGS:  # filter scripts and objects (attack vectors)
            self._excl_nested_level += 1
            return

        self._html.write('<')
        self._html.write(tag)

        for attr in attrs:
            if attr[0].startswith('on'):
                # skip onclick="", on...="" attributes (attack vectors)
                continue
            self._html.write(' ')
            self._html.write(attr[0])
            if attr[1] is not None:
                self._html.write('="')
                if attr[0] == 'src':
                    self._insert_data_uri(attr[1])
                else:
                    self._html.write(attr[1])

                self._html.write('"')

        self._html.write('>')

    def _insert_data_uri(self, src):
        url = parse.unquote(src)
        with self._zip_file.open(url) as src_file:
            src_data = src_file.read()
            src_b64 = base64.b64encode(src_data)

            self._html.write('data:image/png;base64,')
            self._html.write(src_b64.decode('utf-8'))

    def handle_endtag(self, tag):
        if tag in self.FILTERED_TAGS:
            if self._excl_nested_level > 0:
                self._excl_nested_level -= 1
            return

        self._html.write('</')
        self._html.write(tag)
        self._html.write('>')

    def handle_data(self, data):
        if self._excl_nested_level == 0:
            self._html.write(data)

    def final_html(self):
        return self._html.getvalue()
