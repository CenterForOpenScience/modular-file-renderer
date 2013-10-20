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
    
    def _render(self, fp, path, fileType):
        _, filename = os.path.split(fp.name)
        exporters = self.render_exporters(filename, fileType)
        rendered = self.render(fp, path)
        return exporters + '\n' + rendered

    def render_exporters(self, filename, fileType):
        """Render exporters to an HTML form.

        :param filename: Name of file to export fileType: extension of the file
        :return: HTML form with dropdown widget

        """
        if not self.exporters:
            return ''
	
	options = []
	for exporter in self.exporters:
		if exporter != fileType:	
            		options.append('<option value="{}">{}</option>'.format(
                		exporter, exporter.capitalize()
            			))

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
        :return: File type of the file to be rendered (string)

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
