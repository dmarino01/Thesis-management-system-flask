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
        flash("Advisor No Encontrado.", "danger")
        return redirect(url_for('advisor.advisor'))

# Display the create advisor form
@advisor_bp.route('/create_advisor_form', methods=['GET'])
@login_required
def create_advisor_form():
    return render_template('components/advisor/create.html')

# Display the assign author-advisor form
@advisor_bp.route('/assign_author_advisor_form', methods=['GET'])
@login_required
def assign_author_advisor_form():
    return render_template('components/advisor/assign.html')

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
                flash("Asesor Creado Exitosamente.", "success")
                return redirect(url_for('advisor.advisor'))
            else:
                flash("Las contraseñas no coinciden.", "danger")
                return redirect(url_for('advisor.create_advisor_form'))
        else:
            flash("No deben haber campos vacios.", "danger")
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
            flash("Advisor Actualizado Exitosamente...", "success")
            return redirect(url_for('advisor.advisor'))
        else:
            flash("No deben haber campos vacios...", "danger")
            return redirect(url_for('advisor.create_advisor_form'))
    except Exception as ex:
        flash("No se pudo editar el Advisor...", "danger")
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
                flash("Asesor Eliminado Exitosamente...", "success")
                return redirect(url_for('advisor.advisor'))
            except Exception as ex:
                raise Exception(ex)
        else:
            flash("No se pudo eliminar el Asesor...", "danger")
            return redirect(url_for('advisor.advisor'))
    except Exception as ex:
        raise Exception(ex)
    
# Upload Advisors by csv file
@advisor_bp.route("/upload_advisors", methods=["POST"])
@login_required
def upload_advisors():
    try:
        if "csv_file" not in request.files:
            flash("No file part...", "danger")
            return redirect(url_for("advisor.create_advisor_form"))
        csv_file = request.files["csv_file"]
        separator = request.form["Select_separator"]
        codificator = request.form["Select_codificator"]
        if csv_file.filename == "":
            flash("Sin archivo seleccionado.", "danger")
            return redirect(url_for("advisor.create_advisor_form"))
        if csv_file:
            data = ControllerAdvisor.process_csv(db, separator, codificator, csv_file)
            flash("Revisores Subidos Exitosamente.", "success")
            return redirect(url_for("advisor.create_advisor_form"))
    except Exception as ex:
        raise Exception(ex)
    
# Upload Advisors by csv file
@advisor_bp.route("/upload_advisor_assignations", methods=["POST"])
@login_required
def upload_advisor_assignations():
    try:
        if "csv_file" not in request.files:
            flash("No file part...")
            return redirect(url_for("advisor.assign_author_advisor_form"))
        csv_file = request.files["csv_file"]
        separator = request.form["Select_separator"]
        codificator = request.form["Select_codificator"]
        if csv_file.filename == "":
            flash("Sin archivo seleccionado...", "danger")
            return redirect(url_for("advisor.assign_author_advisor_form"))
        if csv_file:
            data = ControllerAdvisor.process_relations_csv(db, separator, codificator, csv_file)
            flash("Relaciones Subidas Exitosamente.", "success")
            return redirect(url_for("advisor.assign_author_advisor_form"))
    except Exception as ex:
        flash(str(ex), "danger")
        return redirect(url_for("advisor.assign_author_advisor_form"))
    

# Save Advisor assignation
@advisor_bp.route("/save_advisor_assignation/<int:id>", methods=["POST"])
@login_required
def save_advisor_assignation(id):
    try:
        advisor = request.form["advisor"]
        if advisor:
            data = ControllerAdvisor.assignRelationAdvisorThesis(db, id, advisor)
            flash("Asesor asignado correctamente...", "success")
        return redirect(url_for("thesis.admin_assigns_advisor_page", id=id))
    except Exception as ex:  
        flash(str(ex), "danger")  # Display the caught exception message
        return redirect(url_for("thesis.admin_assigns_advisor_page", id=id))
    

# Delete Advisor assignation
@advisor_bp.route("/revome_advisor_from_assignment_page/<int:advisor_id>/<int:thesis_id>")
@login_required
def revome_advisor_from_assignment_page(advisor_id, thesis_id):
    try:
        data = ControllerAdvisor.deleteRelationAdvisorThesis(db, advisor_id, thesis_id)
        flash("Asesor removido correctamente.", "success")
        return redirect(url_for("thesis.admin_assigns_advisor_page", id=thesis_id))
    except Exception as ex:  
        flash(str(ex), "danger")  # Display the caught exception message
        return redirect(url_for("thesis.admin_assigns_advisor_page", id=thesis_id))