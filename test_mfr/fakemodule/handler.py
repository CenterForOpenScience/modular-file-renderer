from mfr import core


class FakeHandler(core.FileHandler):

    def detect(self, fp):
        return True
