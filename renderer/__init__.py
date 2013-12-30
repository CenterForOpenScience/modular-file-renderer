import os
import inspect
from hurry.filesize import size

class TooBigError(Exception):
    pass


class FileMeta(type):
    
    def __init__(cls, name, bases, dct):
        
        # Call super-metaclass __init__
        super(FileMeta, cls).__init__(name, bases, dct)
        
        # Initialize class registry and add self
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        if name != 'FileRenderer':
            cls.registry[name] = cls
        
        # Get export methods
        cls.exporters = [
            name.replace('export_', '')
            for name, value in dct.iteritems()
            if name.startswith('export_') and inspect.isfunction(value)
        ]


class FileRenderer(object):

    __metaclass__ = FileMeta

    # MAX_SIZE = 204800
    MAX_SIZE = 1004800

    
    def _check_size(self, file_pointer):
        return os.stat(file_pointer.name).st_size > self.MAX_SIZE

    def _render(self, file_pointer, file_path):

        if self._check_size(file_pointer):
            max_kb = size(self.MAX_SIZE)
            file_kb = size(os.stat(file_pointer.name).st_size)
            return """
        There was an error rendering {}
        <div>This file is too big: Max size = {}; File size = {}</div>
        """.format(file_pointer.name, max_kb, file_kb)

        _, file_name = os.path.split(file_pointer.name)
        exporters = self.render_exporters(file_name)
        rendered = self.render(file_pointer, file_path)
        return exporters + '\n' + rendered

    def _edit(self, file_pointer, file_path):
        _, file_name = os.path.split(file_pointer.name)
        exporters = self.render_exporters(file_name)
        rendered = self.edit(file_pointer, file_path)
        return exporters + '\n' + rendered

    def _save(self, file_pointer, file_path):
        _, filename = os.path.split(file_pointer.name)
        rendered = self.save(file_pointer, file_path)
        return rendered

    def render_exporters(self, file_name):
        """Render exporters to an HTML form.

        :param file_name: Name of file to export
        :return: HTML form with drop down widget

        """
        if not self.exporters:
            return ''
        options = [
            '<option value="{}">{}</option>'.format(
                exporter, exporter.capitalize()
            )
            for exporter in self.exporters
        ]

        html_from_file = open(os.getcwd() + "/renderer/exporter.html").read()
        html_with_data = html_from_file.format(
            klass=self.__class__.__name__,
            filename=file_name,
            options='\n'.join(options))
        return html_with_data

    def detect(self, file_pointer):
        """Detects whether a given file pointer can be rendered by 
        this renderer. Each renderer needs a detect method that at minimum
        checks the file extension, but ideally includes other checks (e.g.,
        mimetype, file encodings, etc).

        :param file_pointer: File pointer
        :return: Can file be rendered? (bool)

        """
        return False

    def render(self, file_pointer, file_path):
        """Renders a file to HTML.

        :param file_pointer: File pointer
        :param file_path: Path to file
        :return: HTML rendition of file

        """
        pass

    def edit(self, file_pointer, file_path):
        """Renders a file to HTML.

        :param file_pointer: File pointer
        :param file_path: Path to file
        :return: HTML rendition of file

        """
        pass

    def save(self, file_pointer, file_path):
        """Renders a file to HTML.

        :param file_pointer: File pointer
        :param file_path: Path to file
        :return: HTML rendition of file

        """
        pass

    #todo make these more useful doc strings to help out new people writing renderers