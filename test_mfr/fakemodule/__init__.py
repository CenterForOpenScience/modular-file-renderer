from mfr import core


class Handler(core.FileHandler):

    def detect(self, fp):
        return True
