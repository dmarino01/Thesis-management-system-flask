from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerAdvisor import ControllerAdvisor
from flask_login import login_required

from config import db

advisor_bp = Blueprint('advisor', __name__)

# Advisor Index
@advisor_bp.route('/advisor')
@login_required
def advisor():
    # Handle the Advisor page logic here
    return render_template('components/advisor/index.html')

# Search for advisors by name
@advisor_bp.route('/search_advisors', methods=['POST'])
@login_required
def search():
    try:
        name = request.form['keyname']
        data = ControllerAdvisor.getAdvisorsbyName(db, name)
        return render_template('components/advisor/resultado.html', filtered_advisors=data)
    except Exception as ex:
        flash("Advisor No Encontrado...")
        return redirect(url_for('advisor.advisor'))

# Display the create advisor form
@advisor_bp.route('/create_advisor_form', methods=['GET'])
@login_required
def create_advisor_form():
    return render_template('components/advisor/create.html')

# Save a new advisor
@advisor_bp.route('/update_advisor/<int:id>', methods=['POST'])
@login_required
def update_advisor(id):
    try:
        advisor_code = request.form['advisor_code']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        grade = request.form['grade']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        ControllerAdvisor.update_advisor(db, id, advisor_code, firstname, lastname, grade, phone, address, email)
        flash("Revisor Actualizado Exitosamente...")
        return redirect(url_for('advisor.advisor'))
    except Exception as ex:
        flash("No se pudo editar el Revisor...")
        return redirect(url_for('advisor.edit_advisor_form', id=id))

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
        grade = request.form['grade']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        ControllerAdvisor.update_advisor(db, id, advisor_code, firstname, lastname, grade, phone, address, email)
        flash("Advisor Actualizado Exitosamente...")
        return redirect(url_for('advisor.advisor'))
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