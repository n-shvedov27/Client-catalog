from flask import render_template, session, request, redirect, url_for
from werkzeug.local import LocalProxy
import os
from werkzeug.utils import secure_filename

from wsgi import app, ALLOWED_EXTENSIONS
from forms import ClientForm
from models import users, clients, create_user, create_client


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ClientForm(request.form)
    username = session.get('username', None)
    user = users.get(username, None)
    return render_template('index.html', user=user, username=username, form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username].password:
            app.logger.info('login')
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'This user is exist<a href="/register">Register</a>'
        create_user(username, password)
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


def file_is_allowed(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_path_from_request(request: LocalProxy) -> str:
    app.logger.info(type(request))
    if 'photo' not in request.files:
        return redirect(request.url)
    file = request.files['photo']
    app.logger.info(type(file))
    if file.filename == '':
        return redirect(request.url)
    if file and file_is_allowed(file.filename):
        filename = secure_filename(file.filename)
        os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    filename = secure_filename(file.filename)
    filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return filename.replace('\\', '/')


@app.route('/create', methods=['POST'])
def create():
    username = session.get('username', None)
    if not username:
        redirect(url_for('login'))
    user = users[username]

    form = ClientForm(request.form)
    if form.validate_on_submit():
        fio = form['fio'].data
        phone = form['phone'].data
        email = form['email'].data

        filepath = get_file_path_from_request(request)
        create_client(fio, phone, email, user, filepath)

    return redirect(url_for('index'))
