from .. import FileRenderer

class TextRenderer(FileRenderer):

    def detect(self, fp):
        fname = fp.name
        for ext in ['txt']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        fname = fp.name
        return '<pre>{}</pre>'.format(fp.read())
