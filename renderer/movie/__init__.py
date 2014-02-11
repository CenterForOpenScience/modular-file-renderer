from .. import FileRenderer


class MovieRenderer(FileRenderer):

    def __init__(self, max_width=None):
        self.max_width = max_width

    def _detect(self, file_pointer):
        for ext in ['avi', 'mp4', 'ogv', 'wmv', 'webm']:
            if file_pointer.name.endswith(ext):
                return True
        return False

    def _render(self, file_pointer, **kwargs):
        url = kwargs['url']
        return '''
               <video width="320" height="240" controls>
               <source src="{file_path}">
               Your browser does not support the video tag.
               </video>
                '''.format(file_path=url)