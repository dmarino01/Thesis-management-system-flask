from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from controllers.ControllerRole import ControllerRole
from controllers.ControllerPermission import ControllerPermission

from config import db

role_bp = Blueprint('role', __name__)

# Role Index
@role_bp.route('/role')
@login_required
def role():
    data = ControllerRole.getRoles(db)
    return render_template('components/role/index.html', roles=data)

# Search for roles by name
@role_bp.route('/search_roles', methods=['POST'])
@login_required
def search_roles():
    try:
        name = request.form['keyname']
        data = ControllerRole.getRolesbyName(db, name)
        return render_template('components/role/resultado.html', filtered_roles=data)
    except Exception as ex:
        flash("Rol No Encontrado...", "danger")
        return redirect(url_for('role.role'))
    
# Display the create role form
@role_bp.route('/create_role_form', methods=['GET'])
@login_required
def create_role_form():
    return render_template('components/role/create.html')

# Save a new role
@role_bp.route('/save_role', methods=['POST'])
@login_required
def save_role():
    try:
        role = request.form['role']
        ControllerRole.createRole(db, role)
        flash("Rol Creado Exitosamente...", "success")
        return redirect(url_for('role.role'))
    except Exception as ex:
        flash("Rol No ha sido Creado...", "danger")
        return redirect(url_for('role.create_role_form'))
    
# Display the edit role form
@role_bp.route('/edit_role_form/<int:id>', methods=['GET'])
@login_required
def edit_role_form(id):
    role = ControllerRole.get_role_by_id(db, id)
    return render_template('components/role/edit.html', role=role)

# Update a role
@role_bp.route('/update_role/<int:id>', methods=['POST'])
@login_required
def update_role(id):
    try:
        role = request.form['role']
        ControllerRole.update_role(db, id, role)
        flash("Role Actualizado Exitosamente...", "success")
        return redirect(url_for('role.role'))
    except Exception as ex:
        flash("No se pudo editar el Role...", "danger")
        return redirect(url_for('role.edit_role_form', id=id))
    
# Display the assign permission to roles form
@role_bp.route('/assign_permission_form/<int:id>', methods=['GET'])
@login_required
def assign_permission_form(id):
    role = ControllerRole.get_role_by_id(db, id)
    permissions = ControllerPermission.getPermissions(db)
    return render_template('components/role/assign.html', role=role, permissions =permissions)

# Save the assigned permissions to the role
@role_bp.route('/save_permissions_for_role/<int:id>', methods=['POST'])
@login_required
def save_permissions_for_role(id):
    try:
        permissions = ""
        ControllerRole.assign_permissions(db, id, permissions)
        flash("Permisos Asignados Correctamente...", "success")
        return redirect(url_for('role.role'))
    except Exception as ex:
        flash("No se guardos los roles...", "danger")
        return redirect(url_for('role.assign_permission_form', id=id))

# Deactivate a role
@role_bp.route('/desactivate_role/<int:id>')
@login_required
def desactivate_role(id):
    try:
        role = ControllerRole.get_role_by_id(db, id)
        if role:
            try:
                ControllerRole.desactivate_role(db, id)
                flash("Rol Eliminado Exitosamente...", "success")
                return redirect(url_for('role.role'))
            except Exception as ex:
                raise Exception(ex)
        else:
            flash("No se pudo eliminar el Rol...", "danger")
            return redirect(url_for('role.role'))
    except Exception as ex:
        raise Exception(ex)