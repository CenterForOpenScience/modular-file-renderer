import os
import abc
import inspect

class FileMeta(abc.ABCMeta):
    
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
            if name.startswith('export_')
                and inspect.isfunction(value)
        ]

class FileRenderer(object):

    __metaclass__ = FileMeta
    
    def _render(self, fp, path):
        
        _, filename = os.path.split(fp.name)
        exporters = self.render_exporters(filename)
        rendered = self.render(fp, path)
        return exporters + '\n' + rendered

    def render_exporters(self, filename):
        """Render exporters to an HTML form.

        :param filename: Name of file to export
        :return: HTML form with dropdown widget

        """
        if not self.exporters:
            return ''

        options = [
            '<option value="{}">{}</option>'.format(
                exporter, exporter.capitalize()
            )
            for exporter in self.exporters
        ]

        return '''
        <form method="post" action="/export/{klass}/{filename}/">
            <select name="exporter">
                {options}
            </select>
            <input type="submit" value="Submit" />
        </form>'''.format(
            klass=self.__class__.__name__,
            filename=filename,
            options='\n'.join(options)
        )

    @abc.abstractmethod
    def detect(self, fp):
        """Detects whether a given file pointer can be rendered by 
        this renderer.

        :param fp: File pointer
        :return: Can file be rendered? (bool)

        """
        pass

    @abc.abstractmethod
    def render(self, fp, path):
        """Renders a file to HTML.

        :param fp: File pointer
        :param path: Path to file
        :return: HTML rendition of file

        """
        pass
