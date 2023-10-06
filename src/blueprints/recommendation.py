from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerRecommendation import ControllerRecommendation
from flask_login import login_required

from config import db

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendation')
@login_required
def recommendation_thesis():
    data = ControllerRecommendation.get_thesis_by_author_advisor(db, 2)
    return render_template('recommendation/index.html', thesis=data)