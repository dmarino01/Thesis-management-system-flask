from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerAdvisor import ControllerAdvisor
from flask_login import login_required

from config import db

advisor_bp = Blueprint('advisor', __name__)

# Advisor Index
@advisor_bp.route('/advisor')
@login_required
def advisor():
    data = ControllerAdvisor.getAdvisors(db)
    return render_template('components/advisor/index.html', advisors = data)

# Search for advisors by name
@advisor_bp.route('/search_advisors', methods=['POST'])
@login_required
def search():
    try:
        name = request.form['keyname']
        data = ControllerAdvisor.getAdvisorsbyName(db, name)
        return render_template('components/advisor/resultado.html', filtered_advisors = data)
    except Exception as ex:
        flash("Advisor No Encontrado...")
        return redirect(url_for('advisor.advisor'))

# Display the create advisor form
@advisor_bp.route('/create_advisor_form', methods=['GET'])
@login_required
def create_advisor_form():
    return render_template('components/advisor/create.html')

# Save a new advisor
@advisor_bp.route('/save_advisor', methods=['POST'])
@login_required
def save_advisor():
    try:
        advisor_code = request.form['advisor_code']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dni = request.form['dni']
        institution = request.form['institution']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        if advisor_code != "" and firstname != "" and lastname != "" and dni != "" and phone != "" and email != "" and username != "" and password != "" and verify_password != "":
            if password == verify_password:
                ControllerAdvisor.createAdvisor(db, advisor_code, firstname, lastname, dni, institution, phone, address, email, username, password)
                flash("Asesor Creado Exitosamente...")
                return redirect(url_for('advisor.advisor'))
            else:
                flash("Las contraseñas no coinciden...")
                return redirect(url_for('advisor.create_advisor_form'))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for('advisor.create_advisor_form'))
    except Exception as ex:
        return redirect(url_for('advisor.create_advisor_form'))

# Display the edit advisor form
@advisor_bp.route('/edit_advisor_form/<int:id>', methods=['GET'])
@login_required
def edit_advisor_form(id):
    advisor = ControllerAdvisor.get_advisor_by_id(db, id)
    return render_template('components/advisor/edit.html', advisor=advisor)

# Update a advisor
@advisor_bp.route('/update_advisor/<int:id>', methods=['POST'])
@login_required
def update_advisor(id):
    try:
        advisor_code = request.form['advisor_code']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dni = request.form['dni']
        institution = request.form['institution']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        username = request.form['username']
        if advisor_code != "" and firstname != "" and lastname != "" and dni != "" and phone != "" and email != "" and username != "":
            ControllerAdvisor.update_advisor(db, id, advisor_code, firstname, lastname, dni, institution, phone, address, email, username)
            flash("Advisor Actualizado Exitosamente...")
            return redirect(url_for('advisor.advisor'))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for('advisor.create_advisor_form'))
    except Exception as ex:
        flash("No se pudo editar el Advisor...")
        return redirect(url_for('advisor.edit_advisor_form', id=id))


# Deactivate an advisor
@advisor_bp.route('/desactivate_advisor/<int:id>')
@login_required
def desactivate_advisor(id):
    try:
        advisor = ControllerAdvisor.get_advisor_by_id(db, id)
        if advisor:
            try:
                ControllerAdvisor.desactivate_advisor(db, id)
                flash("Asesor Eliminado Exitosamente...")
                return redirect(url_for('advisor.advisor'))
            except Exception as ex:
                raise Exception(ex)
        else:
            flash("No se pudo eliminar el Asesor...")
            return redirect(url_for('advisor.advisor'))
    except Exception as ex:
        raise Exception(ex)