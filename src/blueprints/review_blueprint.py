from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerReview import ControllerReview
from flask_login import login_required

from config import db

review_bp = Blueprint('review', __name__)

@review_bp.route('/review')
@login_required
def review_thesis():
    return render_template('review/index.html')