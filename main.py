from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    html = ''
    for fn in os.listdir('examples'):
        html += '<a href="/example/{filename}">{filename}</a><br />'.format(
            filename=fn)
    return html

@app.route('/example/<filename>')
def examples(filename):
    return filename

if __name__ == '__main__':
    app.run(debug=True)