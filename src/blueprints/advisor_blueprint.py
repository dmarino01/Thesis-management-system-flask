from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerAdvisor import ControllerAdvisor
from flask_login import login_required

from config import db

advisor_bp = Blueprint('advisor', __name__)

# Advisor Index
@advisor_bp.route('/advisor')
@login_required
def advisor():
    # Handle the Advisor page logic here
    return render_template('components/advisor/index.html')

# Search for advisors by name

# Display the create advisor form
@advisor_bp.route('/create_advisor_form', methods=['GET'])
@login_required
def create_advisor_form():
    return render_template('components/advisor/create.html')

# Save a new reviewer

# Display the edit reviewer form

# Update a Reviewer
  
# Deactivate a reviewer