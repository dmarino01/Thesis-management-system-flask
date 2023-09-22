from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerPermission import ControllerPermission
from flask_login import login_required

from config import db

permission_bp = Blueprint('permission', __name__)

# Permission Index
@permission_bp.route('/permission')
@login_required
def permission():
    data = ControllerPermission.getPermissions(db)
    return render_template('components/permission/index.html', permissions=data)