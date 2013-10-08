from flask import Flask, send_from_directory
import importlib
import os

from renderer import FileRenderer

app = Flask(__name__, static_folder='examples')

# Recursively import modules
for dirpath, dirnames, filenames in os.walk('renderer'):
    for filename in filenames:
        if filename.endswith('.py'):
            modulename = os.path.join(dirpath, filename)\
                .replace('/', '.')\
                .replace('.py', '')
            importlib.import_module(modulename)

# Optional configuration for renderers
config = {
    'ImageRenderer': {'max_width': '200px'},
}

# Module static files should live in renderer/<module/static
@app.route('/static/<module>/<filename>/')
def send_module_file(module, filename):
    module_static_dir = os.path.join('renderer', module, 'static')
    return send_from_directory(module_static_dir, filename)

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
            return renderer.render(fp, '/examples/{}'.format(filename))
    return filename

if __name__ == '__main__':
    app.run(debug=True, port=5001)
