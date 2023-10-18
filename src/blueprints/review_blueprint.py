from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerReview import ControllerReview
from flask_login import login_required

from config import db

review_bp = Blueprint('review', __name__)

@review_bp.route('/review/<int:id>', methods=['GET'])
@login_required
def review_thesis(id):
    data = ControllerReview.get_thesis_by_author_reviewer(db, id)
    return render_template('review/index.html', thesis=data)

@review_bp.route('/review_thesis_page/<int:id>', methods=['GET'])
@login_required
def review_thesis_page(id):
    data = ControllerThesis.get_thesis_by_id(db, id)
    return render_template('review/review.html', thesis=data)
