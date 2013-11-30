from flask import Flask, request, send_file, send_from_directory, redirect
from cStringIO import StringIO
import importlib
import os
import Image
import random
from PIL import Image

from renderer import FileRenderer

app = Flask(__name__, static_folder='examples')

# # Recursively import modules
for dirpath, dirnames, filenames in os.walk('renderer'):
    for filename in filenames:
        if filename.endswith('.py') and filename != "python.py":
            modulename = os.path.join(dirpath, filename)\
                .replace('/', '.')\
                .replace('.py', '')
            importlib.import_module(modulename)

# Optional configuration for renderers
config = {
    'ImageRenderer': {'max_width': '200px'},
}

# Module static files should live in renderer/<module/static
@app.route('/static/<module>/<path:filepath>')
def send_module_file(module, filepath):
    path, filename = os.path.split(filepath)
    module_static_dir = os.path.join('renderer', module, 'static', path)
    return send_from_directory(module_static_dir, filename)

@app.route('/export/<renderer>/<filename>/', methods=['POST'])
def export(renderer, filename):
    exporter = request.form.get('exporter')
    renderer_class = FileRenderer.registry.get(renderer)
    if exporter == "edit":
        return redirect("/edit/{}".format(filename))
    if exporter == "save":
        return redirect("/save/{}".format(filename))
    if renderer_class is None:
        return 'Renderer not found.'
    renderer_object = renderer_class(**config.get(renderer, {}))
    renderer_method = getattr(
        renderer_object, 
        'export_{}'.format(exporter), 
        None
    )
    if renderer_method is None:
        return 'Renderer exporter not found.'
    filepath = os.path.join('examples', filename)
    rendered, extension = renderer_method(open(filepath))

    name, ext = os.path.splitext(filename)
    export_name = name + extension

    return send_file(
        StringIO(rendered),
        as_attachment=True,
        attachment_filename=export_name,
    )

@app.route('/')
def index():
    html = ''
    for fn in os.listdir('examples'):
        html += '<a href="/render/{filename}">{filename}</a><br />'.format(
            filename=fn)
    return html

@app.route('/render/<filename>')
def render(filename):
    fp = open(os.path.join('examples', filename))
    for name, cls in FileRenderer.registry.items():
        renderer = cls(**config.get(name, {}))
        if renderer.detect(fp):
            return renderer._render(fp, '/examples/{}?{}'.format(
                filename, random.random()))
    return filename

@app.route('/edit/<filename>')
def edit(filename):
    fp = open(os.path.join('examples', filename))
    for name, cls in FileRenderer.registry.items():
        renderer = cls(**config.get(name, {}))
        if renderer.detect(fp):
            return renderer._edit(fp, '/examples/{}?{}'.format(
                filename, random.random()))
    return filename

# @app.route('/edit/save/<filename>', methods=['POST'])
# def edit_save(filename):
#     file = open("examples/{}".format(filename),'w')
#     file.write(str(request.json))
#     file.close()
#     return ""

@app.route('/save/<filename>', methods=['POST'])
def save(filename):
    fp = open(os.path.join('examples', filename))
    for name, cls in FileRenderer.registry.items():
        renderer = cls(**config.get(name, {}))
        if renderer.detect(fp):
            return renderer._save(fp, '/examples/{}?{}'.format(
                filename, random.random()))
    return filename

if __name__ == '__main__':
    app.run(debug=True, port=5001)


