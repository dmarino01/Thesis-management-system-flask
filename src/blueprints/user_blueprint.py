from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from controllers.ControllerUser import ControllerUser
from controllers.ControllerAdmin import ControllerAdmin
from controllers.ControllerAuthor import ControllerAuthor
from controllers.ControllerAdvisor import ControllerAdvisor
from controllers.ControllerReviewer import ControllerReviewer
from models.User import User

from config import db

user_bp = Blueprint('user', __name__)


# Route for Login in
@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'],
                    request.form['password'], 0, 0)
        logged_user = ControllerUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Contraseña Inválida...', 'error')
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


# Open form for user edition
@user_bp.route('/profile')
@login_required
def profile():
    data = ""
    id = current_user.person_id
    if current_user.role == "Admin":
        data = ControllerAdmin.get_admin_by_person_id(db, id)
    if current_user.role == "Autor":
        data = ControllerAuthor.get_author_by_person_id(db, id)
    elif current_user.role == "Asesor":
        data = ControllerAdvisor.get_advisor_by_person_id(db, id)
    elif current_user.role == "Revisor":
        data = ControllerReviewer.get_reviewer_by_person_id(db, id)
    return render_template('profile.html', user=data)


# Route to update user
@user_bp.route('/edit_user/<int:id>', methods=['POST'])
@login_required
def edit_user(id):
    try:
        student_code = ''
        advisor_code = ''
        reviewer_code = ''
        grade = ''
        if current_user.role == "Autor":
            student_code = request.form['student_code']
        elif current_user.role == "Asesor":
            advisor_code = request.form['advisor_code']
        elif current_user.role == "Revisor":
            reviewer_code = request.form['reviewer_code']
            grade = request.form['grade']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dni = request.form['dni']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        if username != "":
            if password == verify_password:
                ControllerUser.update_user(db, id, student_code, reviewer_code, advisor_code, grade, firstname, lastname, dni, phone, address, email, username, password)
                flash("Perfil Actualizado Exitosamente...")
                return redirect(url_for('user.profile'))
            else:
                flash("Las contraseñas no coinciden...")
                return redirect(url_for('user.profile'))
        else:
            flash("Usuario no debe estar vacio...")
            return redirect(url_for('user.profile'))
    except:
        return redirect(url_for('user.profile'))
