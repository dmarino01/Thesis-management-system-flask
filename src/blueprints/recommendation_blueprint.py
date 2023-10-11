import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerRecommendation import ControllerRecommendation
from flask_login import current_user, login_required

from config import db

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendation')
@login_required
def recommendation_thesis():
    data = ControllerRecommendation.get_thesis_by_author_advisor(db, 2)
    return render_template('recommendation/index.html', thesis=data)

@recommendation_bp.route('/save_recommendation/<int:id>', methods=['POST'])
@login_required
def save_recommendation(id):
    try:
        recommendation_text = request.form['text']
        date = datetime.datetime.now()
        thesis_id = id
        person_id = current_user.person_id
        ControllerRecommendation.createRecommendation(db, recommendation_text, date, thesis_id, person_id)
        flash("Recomendación Guardada correctamente...")
        return redirect(url_for('thesis.view_thesis_page', id=id))
    except Exception as ex:
        raise Exception(ex)