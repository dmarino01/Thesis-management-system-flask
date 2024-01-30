import base64
from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_required
from datetime import timedelta
from jinja2 import Environment, FileSystemLoader
from config import Config, db, csrf

# Controller:
from controllers.ControllerUser import ControllerUser

# Blueprints:
from blueprints.author_blueprint import author_bp
from blueprints.reviewer_blueprint import reviewer_bp
from blueprints.advisor_blueprint import advisor_bp
from blueprints.role_blueprint import role_bp
from blueprints.permission_blueprint import permission_bp
from blueprints.thesis_blueprint import thesis_bp
from blueprints.user_blueprint import user_bp
from blueprints.review_blueprint import review_bp
from blueprints.recommendation_blueprint import recommendation_bp
from blueprints.report_blueprint import report_bp

app = Flask(__name__)

app.config.from_object(Config)

app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

UPLOAD_FOLDER = '/static/file/thesis/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.url_map.strict_slashes = False

db.init_app(app)

app.register_blueprint(author_bp)
app.register_blueprint(advisor_bp)
app.register_blueprint(reviewer_bp)
app.register_blueprint(role_bp)
app.register_blueprint(permission_bp)
app.register_blueprint(thesis_bp)
app.register_blueprint(user_bp)
app.register_blueprint(review_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(report_bp)

login_manager_app=LoginManager(app)

env = Environment(loader=FileSystemLoader("templates"))

@login_manager_app.user_loader
def load_user(user_id):
    user = ControllerUser.get_by_id(db, user_id)
    if user:
        user.decoded_image = user.decode_image()  # Decode the image and store it in the user object
    return user

@app.route('/')
@app.route('/index')
@login_required
def home():
    return render_template("home.html")

def status_401(error):
    return redirect(url_for('user.login'))

def status_404(error):
    return render_template("404.html")

@app.route("/register")
def register():
    return render_template("auth/register.html")

@app.route("/registerUser")
def registerUser():
    return redirect(url_for('user.login'))

@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html')

@app.route('/temas')
@login_required
def temas():
    return render_template('temas.html')

@app.route('/libreria')
@login_required
def libreria():
    return render_template('libreria.html')

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

@app.route('/download/<path:filename>')
def download_file(filename):
    static_folder = 'static'
    return send_from_directory(static_folder, filename, as_attachment=True)


if __name__ == '__main__':
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()