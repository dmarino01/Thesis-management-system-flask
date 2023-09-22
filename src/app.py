from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from config import Config, db, csrf

# Controller:
from controllers.ControllerUser import ControllerUser

# Entities:
from models.User import User

# Blueprints:
from blueprints.author_blueprint import author_bp
from blueprints.reviewer_blueprint import reviewer_bp
from blueprints.advisor_blueprint import advisor_bp

app = Flask(__name__)

app.config.from_object(Config)

app.url_map.strict_slashes = False

db.init_app(app)

app.register_blueprint(author_bp)
app.register_blueprint(advisor_bp)
app.register_blueprint(reviewer_bp)


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
    return redirect(url_for('login'))

def status_404(error):
    return render_template("404.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'], 0)
        logged_user=ControllerUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash ('Contraseña Inválida...', 'error')
                return render_template("auth/login.html")
        else:
            flash('Usuario No Encontrado...', 'error')
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register")
def register():
    return render_template("auth/register.html")

@app.route("/registerUser")
def registerUser():
    #Logic
    return redirect(url_for('login'))

@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/temas')
@login_required
def temas():
    return render_template('temas.html')

@app.route('/libreria')
@login_required
def libreria():
    return render_template('libreria.html')

# START TESIS ROUTES
@app.route('/tesis')
@login_required
def tesis():
    # Handle the library page logic here
    return render_template('components/tesis/index.html')

# END ROUTES COMPONENTS

if __name__ == '__main__':
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()