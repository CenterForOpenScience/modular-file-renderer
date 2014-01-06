OSF Modular File Renderer
=====================
Our priority is to be robust to many kinds of research across many domains, so we host many file types.

The modular file renderer makes it possible for people to easily build independent means of previewing and sometimes editing and/or exporting files uploaded to the OSF. The renderer directory already contains several working examples you can examine for ideas and extrapolate from in building your own, whatever your specialty or interest.

##Getting Started

After you fork this repository, you'll want to inspect the directories for whether the rendering you'd like to go after has already been started. It'd be under "renderer." Otherwise, you should start your own directory under "renderer" and look at the code in __init__.py, from which you'll subclass FileRenderer for your own "detect" and "render" methods, as in this example with simple text rendering:

```python
from .. import FileRenderer


class TextRenderer(FileRenderer):

    def detect(self, file_pointer):
        file_name = file_pointer.name
        if file_name.endswith('.txt'):
            return True
        return False

    def render(self, file_pointer, file_path):
        return '<pre>{}</pre>'.format(file_pointer.read())

    def export_text(self, file_pointer):
        return file_pointer.read(), '.txt'
```

##Issue Tracking (bug reports, suggestions, requests)

Whether you're a developer who knows of interesting libraries for file rendering or a scientist with a need for particular file support, or both, feel free to make suggestions on our [Issue Tracker](https://github.com/CenterForOpenScience/modular-file-renderer/issues?state=open).

When you build your own renderer, keep track of its progress here by modifying this readme when you push changes.
##
| renderer          | filetype(s)        | status                          |
| :---------------: | :----------------: | :-----------------------------: |
| PDF               | .pdf               |                                 |
| tabular           | .csv, .xlsx        |                                 |
| image             | .jpg, .png         |                                 |
| code              | .py, .rb, .R       |                                 |
| docx              | .docx              | render, no edit, export to html |