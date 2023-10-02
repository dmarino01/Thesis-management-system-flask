from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required
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

app = Flask(__name__)

app.config.from_object(Config)

app.url_map.strict_slashes = False

db.init_app(app)

app.register_blueprint(author_bp)
app.register_blueprint(advisor_bp)
app.register_blueprint(reviewer_bp)
app.register_blueprint(role_bp)
app.register_blueprint(permission_bp)
app.register_blueprint(thesis_bp)
app.register_blueprint(user_bp)

login_manager_app=LoginManager(app)

@login_manager_app.user_loader
def load_user(user_id):
    return ControllerUser.get_by_id(db, user_id)

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

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/temas')
@login_required
def temas():
    return render_template('temas.html')

@app.route('/libreria')
@login_required
def libreria():
    return render_template('libreria.html')

@app.route('/tesis')
@login_required
def tesis():
    return render_template('components/tesis/index.html')

if __name__ == '__main__':
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()