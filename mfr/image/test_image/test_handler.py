from mfr.image.handler import ImageFileHandler


def test_image_handler_detect_image(fakefile):
    # set the file's name
    fakefile.name = 'myimage.jpg'

    handler = ImageFileHandler()
    assert handler.detect(fakefile) is True
