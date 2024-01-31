from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerReview import ControllerReview
from flask_login import current_user, login_required
import datetime

from config import db

review_bp = Blueprint('review', __name__)


# View Thesis per reviewer
@review_bp.route('/review/<int:id>', methods=['GET'])
@login_required
def review_thesis(id):
    data = ControllerReview.get_thesis_by_review_reviewer(db, id)
    return render_template('review/index.html', thesis=data)


# View to Review Thesis
@review_bp.route('/review_thesis_page/<int:id>', methods=['GET'])
@login_required
def review_thesis_page(id):
    person_id = current_user.person_id
    data = ControllerThesis.get_thesis_by_id(db, id)
    review_exists = ControllerReview.check_review_exists(db, id, person_id)
    return render_template('review/review.html', thesis=data, review_exists = review_exists)


# Route to save review
@review_bp.route('/save_review/<int:id>', methods=['GET', 'POST'])
@login_required
def save_review(id):
    try:
        person_id = current_user.person_id
        nota = request.form['nota']
        comentario = request.form['comentario']
        date = datetime.datetime.now()
        ControllerReview.createReview(db, nota, comentario, id, person_id, date)
        flash("Nota Guardada", "success")
        return redirect(url_for('review.review_thesis', id=person_id))
    except Exception as ex:
        raise Exception(ex)
