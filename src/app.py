from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required


from config import config

# Models:
from controllers.ControllerUser import ControllerUser
from controllers.ControllerAutor import ControllerAutor
#from controllers.ControllerTesis import ControllerTesis
#from controllers.ControllerCritico import ControllerCritico
#from controllers.ControllerRevision import ControllerRevision
#from controllers.ControllerAsesor import ControllerAsesor

# Entities:
from models.User import User
from models.Autor import Autor

app = Flask(__name__)



csrf = CSRFProtect()
app.url_map.strict_slashes = False

db = MySQL(app)
login_manager_app=LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ControllerUser.get_by_id(db, id)

@app.route('/')
@app.route('/index')
@login_required
def home():
    #return redirect(url_for('login'))
    return render_template("home.html")

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return render_template("404.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0, request.form['username'], 0, request.form['password'])
        logged_user=ControllerUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash ("Contraseña Inválida...")
                return render_template("auth/login.html")
        else:
            flash("Usuario No Encontrado...")
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
    # Handle the usuarios page logic here
    return render_template('usuarios.html')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/temas')
@login_required
def temas():
    # Handle the temas page logic here
    return render_template('temas.html')

@app.route('/libreria')
@login_required
def libreria():
    # Handle the librery page logic here
    return render_template('libreria.html')

# START ROUTES COMPONENTS
@app.route('/tesis')
@login_required
def tesis():
    # Handle the library page logic here
    return render_template('components/tesis/index.html')

@app.route('/autor')
@login_required
def autor():
    # Handle the author page logic here
    data = ControllerAutor.getAutors(db)
    return render_template('components/autor/index.html', autores = data)

@app.route('/asesor')
@login_required
def asesor():
    # Handle the Authors page logic here
    return render_template('components/asesor/index.html')

@app.route('/review')
@login_required
def review():
    # Handle the Authors page logic here
    return render_template('components/review/index.html')

@app.route('/reviewer')
@login_required
def reviewer():
    # Handle the Authors page logic here
    return render_template('components/reviewer/index.html')
# END ROUTES COMPONENTS

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()


