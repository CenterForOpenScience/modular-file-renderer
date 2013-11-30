from .. import FileRenderer
from cStringIO import StringIO
import Image


class MovieRenderer(FileRenderer):

    def __init__(self, max_width=None):
        self.max_width = max_width

    def detect(self, fp):
        fname = fp.name
        for ext in ['avi','mp4','ogv', 'wmv', 'webm']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        fname = fp.name
        print fp.name
        return '''
               <video width="320" height="240" controls>
               <source src="{}">
               Your browser does not support the video tag.
               </video>
                '''.format(path)

