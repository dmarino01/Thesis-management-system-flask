from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from controllers.ControllerUser import ControllerUser
from models.User import User
from flask_login import login_required

from config import db

user_bp = Blueprint('user', __name__)

# Route for Login in
@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'], 0, 0)
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
    
# Route for Logout
@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

#
@user_bp.route('/edit_user/<int:id>', methods=['POST'])
@login_required
def edit_user(id):
    try:
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        if username != "":
            if password == verify_password:
                ControllerUser.update_user(db, id, username, password)
                #Blue or successful alert
                flash("Perfil Actualizado Exitosamente...")
                return redirect(url_for('profile'))
            else:
                #Red or unsuccessful alert
                flash("Las contraseñas no coinciden...")
                return redirect(url_for('profile'))
        else:
            #Red or unsuccessful alert
            flash("Usuario no debe estar vacio...")
            return redirect(url_for('profile'))
    except:
        return redirect(url_for('profile'))