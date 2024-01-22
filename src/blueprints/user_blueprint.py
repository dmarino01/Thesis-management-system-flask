import base64
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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
    try:
        if request.method == 'POST':
            user = User(0, request.form['username'], request.form['password'], 0, 0, 0)
            logged_user = ControllerUser.login(db, user)
            if logged_user != None:
                if logged_user.password:
                    login_user(logged_user)
                    #flash('Login exitoso!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Contraseña Inválida...', 'danger')
                    return render_template("auth/login.html")
            else:
                flash('Usuario No Encontrado...', 'danger')
                return render_template("auth/login.html")
        else:
            return render_template("auth/login.html")
    except Exception as ex:
        raise Exception(ex)


# Route for Logout
@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Salio de la sessión correctamente...", "info")
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
        data = ControllerAuthor.get_autor_by_id(db, id)
    elif current_user.role == "Asesor":
        data = ControllerAdvisor.get_advisor_by_id(db, id)
    elif current_user.role == "Revisor":
        data = ControllerReviewer.get_reviewer_by_id(db, id)

    # Encode the image data to base64
    if data and data['image']:
        image_data = base64.b64encode(data['image']).decode('utf-8')
    else:
        image_data = None
    return render_template('profile.html', user=data, image_data=image_data)


# Route to update user
@user_bp.route('/edit_user/<int:id>', methods=['POST'])
@login_required
def edit_user(id):

    student_code = ''
    advisor_code = ''
    reviewer_code = ''
    grade = ''
    institution = ''

    if current_user.role == "Autor":
        student_code = request.form['student_code']
    elif current_user.role == "Asesor":
        advisor_code = request.form['advisor_code']
        institution = request.form['institution']
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

    if 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename != '':
            # Validate the file extension
            if not allowed_img(image_file.filename):
                flash("Formato de Archivo Inválido. Seleccione una imagee (e.g., .jpg, .png, .jpeg).", "danger")
                return redirect(url_for('user.profile'))
            image = image_file.read()
        else:
            image = None
    else:
        image = None

    if (current_user.role == "Admin" or
        (current_user.role == "Autor" and student_code != "") or
        (current_user.role == "Asesor" and advisor_code != "") or
        (current_user.role == "Revisor" and reviewer_code != "" and grade != "")):
        
        if firstname != "" and lastname != "" and dni != "" and email != "" and username != "":
            if password == verify_password:
                ControllerUser.update_user(db, id, student_code, reviewer_code, advisor_code, institution, grade, firstname, lastname, dni, phone, address, email, image, username, password)
                flash("Perfil Actualizado Exitosamente...", "success")
                return redirect(url_for('user.profile'))
            else:
                flash("Las contraseñas no coinciden...", "danger")
                return redirect(url_for('user.profile'))
        else:
            flash("Usuario no debe estar vacio...", "danger")
            return redirect(url_for('user.profile'))
    else:
        flash("Campo de código/grado faltante(s)...", "danger")
        return redirect(url_for('user.profile'))

# Route to remove image user
@user_bp.route('/remove_image_user/<int:id>')
@login_required
def remove_image_user(id):
    ControllerUser.remove_image_user(db, id)
    flash("Imagen Removida Exitosamente...", "success")
    return redirect(url_for('user.profile'))

#Function to check if the file extension is allowed
def allowed_img(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions