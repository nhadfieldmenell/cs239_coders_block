from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)
from werkzeug import secure_filename
import os
from generate_code_context import get_code_context
from scoring_script import get_scores

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)


app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    if endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file')
        f = request.files['file']
        code_context = get_code_context(f.read())
        results = get_scores(code_context)
        sample_result = ["http://stackoverflow.com/questions/10171844","http://stackoverflow.com/questions/10154362","http://stackoverflow.com/questions/8922060",
        "http://stackoverflow.com/questions/15524902", "http://stackoverflow.com/questions/10218953"]
        return jsonify(results=results)

@app.route('/uploadajax', methods=['POST'])
def upldfile():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                updir = os.path.join(basedir, 'upload/')
                f.save(os.path.join(updir, filename))
                file_size = os.path.getsize(os.path.join(updir, filename))
            else:
                app.logger.info('ext name error')
                return jsonify(error='ext name error')
        return jsonify(name=filename, size=file_size)


if __name__ == '__main__':
    app.run(debug=False)
