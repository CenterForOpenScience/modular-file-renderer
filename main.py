from flask import Flask, request, send_file, send_from_directory, redirect
from cStringIO import StringIO
import os
from urllib import quote
from renderer import FileRenderer
import importlib
from renderer import image, tabular

app = Flask(__name__, static_folder='examples')

# Recursively import modules
# for dir_path, dir_names, file_names in os.walk('renderer'):
#     for file_name in file_names:
#         if file_name.endswith('.py') and file_name != "python.py" and file_name !="test.py":
#             module_name = os.path.join(dir_path, file_name) \
#                 .replace('/', '.') \
#                 .replace('.py', '')
#             importlib.import_module(module_name)

# Optional configuration for renderers
config = {}

# Module static files should live in renderer/<module/static
@app.route('/static/<module>/<path:file_path>')
def send_module_file(module, file_path):
    file_path, file_name = os.path.split(file_path)
    module_static_dir = os.path.join('renderer', module, 'static', file_path)
    return send_from_directory(module_static_dir, file_name)


@app.route('/export/<renderer>/<file_name>/', methods=['POST'])
def export(renderer, file_name):
    exporter = request.form.get('exporter')
    renderer_class = FileRenderer.registry.get(renderer)
    if exporter == "edit":
        return redirect("/edit/{}".format(file_name))
    if exporter == "save":
        return redirect("/save/{}".format(file_name))
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
    file_path = os.path.join('examples', file_name)
    rendered, extension = renderer_method(open(file_path))

    file_name, file_ext = os.path.splitext(file_name)
    export_name = file_name + extension

    return send_file(
        StringIO(rendered),
        as_attachment=True,
        attachment_filename=export_name,
        )


@app.route('/')
def index():
    html = ''
    for file_name in os.listdir('examples'):
        safe_name = quote(file_name)
        html += '<a href="/render/{safe_name}">{file_name}</a><br />'.format(
             safe_name=safe_name, file_name=file_name)
    return html


@app.route('/render/<file_name>')
def render(file_name):
    file_path = open(os.path.join('examples', file_name))
    print FileRenderer.registry.items()
    for name, cls in FileRenderer.registry.items():
        renderer = cls(**config.get(name, {}))
        if renderer._detect(file_path):
            return renderer._render(file_path, url='/examples/{}'.format(
                file_name))
    return file_name

#
# @app.route('/edit/<file_name>')
# def edit(file_name):
#     file_path = open(os.path.join('examples', file_name))
#     for name, cls in FileRenderer.registry.items():
#         renderer = cls(**config.get(name, {}))
#         if renderer.detect(file_path):
#             return renderer._edit(file_path, '/examples/{}?{}'.format(
#                 file_name, random.random()))
#     return file_name
#
#
# @app.route('/save/<file_name>', methods=['POST'])
# def save(file_name):
#     file_path = open(os.path.join('examples', file_name))
#     for name, cls in FileRenderer.registry.items():
#         renderer = cls(**config.get(name, {}))
#         if renderer.detect(file_path):
#             return renderer._save(file_path, '/examples/{}?{}'.format(
#                 file_name, random.random()))
#     return file_name

if __name__ == '__main__':
    app.run(debug=True, port=5001)


