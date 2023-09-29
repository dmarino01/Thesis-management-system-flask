from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerPermission import ControllerPermission

from config import db

thesis_bp = Blueprint('thesis', __name__)

#Thesis Index
@thesis_bp.route('/myThesis')
@login_required
def myThesis():
    data = ControllerThesis.getThesis(db)
    return render_template("myThesis/index.html", thesis=data)