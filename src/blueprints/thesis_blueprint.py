from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerRecommendation import ControllerRecommendation

from config import db

thesis_bp = Blueprint('thesis', __name__)

#Thesis Index
@thesis_bp.route('/myThesis')
@login_required
def myThesis():
    data = ControllerThesis.getThesis(db)
    return render_template("myThesis/index.html", thesis=data)

#View Thesis
@thesis_bp.route('/view_thesis_page/<int:id>', methods=['GET'])
@login_required
def view_thesis_page(id):
    thesis = ControllerThesis.get_thesis_by_id(db, id)
    recommendation = ControllerRecommendation.get_recommendation_by_thesis_id(db, id)
    return render_template("myThesis/detail.html", thesis=thesis, recommendation = recommendation)

#Thesis Create Form
@thesis_bp.route('/create_thesis_form')
@login_required
def create_thesis_form():
    return render_template("myThesis/create.html")