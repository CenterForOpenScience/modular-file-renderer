"""Video renderer module."""
from mfr.core_methods import RenderResult


def render_movie_tag(fp, src=None):
    """ A simple video renderer.

    :param fp: File pointer
    :param src: Path to source file
    :return: A RenderResult object with an html <video> tag for content
    """

    src = src or fp.name

    content = '''
          <video width="320" height="240" controls>
              <source src="{file_path}">
              Your browser does not support the video tag.
              </video>
              '''.format(file_path=src)
    return RenderResult(content=content)

class MovieProvider:

    def __new__():
        pass
