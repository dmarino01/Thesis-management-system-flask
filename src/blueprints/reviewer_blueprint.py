from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerReviewer import ControllerReviewer
from flask_login import login_required

from config import db

reviewer_bp = Blueprint('reviewer', __name__)

# Reviewer Index
@reviewer_bp.route('/reviewer')
@login_required
def reviewer():
    data = ControllerReviewer.getReviewers(db)
    return render_template('components/reviewer/index.html', reviewers=data)

# Search for reviewers by name
@reviewer_bp.route('/search_reviewers', methods=['POST'])
@login_required
def search():
    try:
        name = request.form['keyname']
        data = ControllerReviewer.getReviewersbyName(db, name)
        return render_template('components/reviewer/resultado.html', filtered_reviewers=data)
    except Exception as ex:
        flash("Reviewer No Encontrado...")
        return redirect(url_for('reviewer.reviewer'))

# Display the create reviewer form
@reviewer_bp.route('/create_reviewer_form', methods=['GET'])
@login_required
def create_reviewer_form():
    return render_template('components/reviewer/create.html')

# Save a new reviewer
@reviewer_bp.route('/save_reviewer', methods=['POST'])
@login_required
def save_reviewer():
    try:
        reviewer_code = request.form['reviewer_code']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        grade = request.form['grade']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        ControllerReviewer.createReviewer(db, reviewer_code, firstname, lastname, grade, phone, address, email)
        flash("Revisor Creado Exitosamente...")
        return redirect(url_for('reviewer.reviewer'))
    except Exception as ex:
        flash("Revisor No ha sido Creado...")
        return redirect(url_for('reviewer.create_reviewer_form'))

# Display the edit reviewer form
@reviewer_bp.route('/edit_reviewer_form/<int:id>', methods=['GET'])
@login_required
def edit_reviewer_form(id):
    reviewer = ControllerReviewer.get_reviewer_by_id(db, id)
    return render_template('components/reviewer/edit.html', reviewer=reviewer)

# Update a reviewer
@reviewer_bp.route('/update_reviewer/<int:id>', methods=['POST'])
@login_required
def update_reviewer(id):
    try:
        reviewer_code = request.form['reviewer_code']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        grade = request.form['grade']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        ControllerReviewer.update_reviewer(db, id, reviewer_code, firstname, lastname, grade, phone, address, email)
        flash("Revisor Actualizado Exitosamente...")
        return redirect(url_for('reviewer.reviewer'))
    except Exception as ex:
        flash("No se pudo editar el Revisor...")
        return redirect(url_for('reviewer.edit_reviewer_form', id=id))
  
# Deactivate a reviewer
@reviewer_bp.route('/desactivate_reviewer/<int:id>')
@login_required
def desactivate_reviewer(id):
    try:
        reviewer = ControllerReviewer.get_reviewer_by_id(db, id)
        if reviewer:
            try:
                ControllerReviewer.desactivate_reviewer(db, id)
                flash("Revisor Eliminado Exitosamente...")
                return redirect(url_for('reviewer.reviewer'))
            except Exception as ex:
                raise Exception(ex)
        else:
            flash("No se pudo eliminar el Revisor...")
            return redirect(url_for('reviewer.reviewer'))
    except Exception as ex:
        raise Exception(ex)