"""Movie renderer module."""
from mfr.core import RenderResult


def render_movie_tag(fp, src=None):
    content = '''
              <video width="320" height="240" controls>
              <source src="{file_path}">
              Your browser does not support the video tag.
              </video>
              '''.format(file_path=src)
    return RenderResult(content=content)
