import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerRecommendation import ControllerRecommendation
from controllers.ControllerThesis import ControllerThesis
from flask_login import current_user, login_required

from config import db

recommendation_bp = Blueprint('recommendation', __name__)

sections = {
    'introduccion': 'Introducción',
    'antecedentes': 'Antecedentes',
    'objetivo': 'Objetivo o Hipotesis',
    'metodo': 'Método',
    'resultados': 'Resultados',
    'discusion': 'Discusión',
    'conclusion': 'Conclusión'
}

@recommendation_bp.route('/recommendation/<int:id>', methods=['GET'])
@login_required
def recommendation_thesis(id):
    try:
        data = ControllerRecommendation.get_thesis_by_author_advisor(db, id)
        return render_template('recommendation/index.html', thesis=data)
    except Exception as ex:
        raise Exception(ex)

@recommendation_bp.route('/save_recommendation/<int:id>', methods=['POST'])
@login_required
def save_recommendation(id):
    try:
        recommendation_text = request.form['text']
        date = datetime.datetime.now()
        thesis_id = id
        person_id = current_user.person_id
        if recommendation_text:
            ControllerRecommendation.createRecommendation(db, recommendation_text, date, thesis_id, person_id)
        return redirect(url_for('thesis.view_thesis_page', id=id))
    except Exception as ex:
        raise Exception(ex)
    
@recommendation_bp.route('/desactivate_recommendation/<int:id>/<int:thesis_id>')
@login_required
def desactivate_recommendation(id, thesis_id):
    try:
        ControllerRecommendation.desactivate_recommendation(db, id)
        return redirect(url_for('thesis.view_thesis_page', id=thesis_id))
    except Exception as ex:
        raise Exception(ex)
    

@recommendation_bp.route('/authorize_review/<int:id>')
@login_required
def authorize_review(id):
    try:
        ControllerRecommendation.authorize_review(db, id)
        return redirect(url_for('thesis.view_thesis_page', id=id))
    except Exception as ex:
        raise Exception(ex)
    

@recommendation_bp.route('/clearing_recommendation/<int:id>/<int:thesis_id>')
@login_required
def clearing_recommendation(id, thesis_id):
    try:
        ControllerRecommendation.clear_recommendation(db, id)
        return redirect(url_for('thesis.view_thesis_page', id=thesis_id))
    except Exception as ex:
        raise Exception(ex)
    
@recommendation_bp.route('/create_recommendation_form/<int:id>')
@login_required
def create_recommendation_form(id):
    data = ControllerThesis.get_thesis_by_id(db, id)
    return render_template("recommendation/recommendation.html", thesis=data)


@recommendation_bp.route('/save_multiple_recommendations/<int:id>', methods=['POST'])
@login_required
def save_multiple_recommendations(id):
    try:
        date = datetime.datetime.now()
        thesis_id = id
        person_id = current_user.person_id

        for section, label in sections.items():
            content = request.form.get(section, '').strip()
            if content:
                recommendation_text = f"{label}: {content}"
                ControllerRecommendation.createRecommendation(db, recommendation_text, date, thesis_id, person_id)

        return redirect(url_for('thesis.view_thesis_page', id=id))
    except Exception as ex:
        raise Exception(ex)