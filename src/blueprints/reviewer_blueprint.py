from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.ControllerReviewer import ControllerReviewer
from flask_login import login_required

from config import db

reviewer_bp = Blueprint("reviewer", __name__)


# Reviewer Index
@reviewer_bp.route("/reviewer")
@login_required
def reviewer():
    data = ControllerReviewer.getReviewers(db)
    return render_template("components/reviewer/index.html", reviewers=data)


# Search for reviewers by name
@reviewer_bp.route("/search_reviewers", methods=["POST"])
@login_required
def search():
    try:
        name = request.form["keyname"]
        data = ControllerReviewer.getReviewersbyName(db, name)
        return render_template(
            "components/reviewer/resultado.html", filtered_reviewers=data
        )
    except Exception as ex:
        flash("Reviewer No Encontrado...")
        return redirect(url_for("reviewer.reviewer"))


# Display the create reviewer form
@reviewer_bp.route("/create_reviewer_form", methods=["GET"])
@login_required
def create_reviewer_form():
    return render_template("components/reviewer/create.html")


# Display the assign reviewer-thesis form
@reviewer_bp.route("/assign_reviewer_thesis_form", methods=["GET"])
@login_required
def assign_reviewer_thesis_form():
    return render_template("components/reviewer/assign.html")


# Save a new reviewer
@reviewer_bp.route("/save_reviewer", methods=["POST"])
@login_required
def save_reviewer():
    try:
        reviewer_code = request.form["reviewer_code"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dni = request.form["dni"]
        grade = request.form["grade"].upper()
        phone = request.form["phone"]
        address = request.form["address"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        verify_password = request.form["verify_password"]
        if (
            reviewer_code != ""
            and firstname != ""
            and lastname != ""
            and dni != ""
            and phone != ""
            and email != ""
            and username != ""
            and password != ""
            and verify_password != ""
        ):
            if password == verify_password:
                ControllerReviewer.createReviewer(
                    db,
                    reviewer_code,
                    firstname,
                    lastname,
                    dni,
                    grade,
                    phone,
                    address,
                    email,
                    username,
                    password,
                )
                flash("Revisor Creado Exitosamente...")
                return redirect(url_for("reviewer.reviewer"))
            else:
                flash("Las contraseñas no coinciden...")
                return redirect(url_for("reviewer.create_reviewer_form"))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for("reviewer.create_reviewer_form"))
    except Exception as ex:
        return redirect(url_for("reviewer.create_reviewer_form"))


# Display the edit reviewer form
@reviewer_bp.route("/edit_reviewer_form/<int:id>", methods=["GET"])
@login_required
def edit_reviewer_form(id):
    reviewer = ControllerReviewer.get_reviewer_by_id(db, id)
    return render_template("components/reviewer/edit.html", reviewer=reviewer)


# Update a reviewer
@reviewer_bp.route("/update_reviewer/<int:id>", methods=["POST"])
@login_required
def update_reviewer(id):
    try:
        reviewer_code = request.form["reviewer_code"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dni = request.form["dni"]
        grade = request.form["grade"].upper()
        phone = request.form["phone"]
        address = request.form["address"]
        email = request.form["email"]
        username = request.form["username"]
        if (
            reviewer_code != ""
            and firstname != ""
            and lastname != ""
            and dni != ""
            and grade != ""
            and phone != ""
            and email != ""
            and username != ""
        ):
            ControllerReviewer.update_reviewer(
                db,
                id,
                reviewer_code,
                firstname,
                lastname,
                dni,
                grade,
                phone,
                address,
                email,
                username,
            )
            flash("Revisor Actualizado Exitosamente...")
            return redirect(url_for("reviewer.reviewer"))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for("reviewer.create_reviewer_form"))
    except Exception as ex:
        return redirect(url_for("reviewer.edit_reviewer_form", id=id))


# Deactivate a reviewer
@reviewer_bp.route("/desactivate_reviewer/<int:id>")
@login_required
def desactivate_reviewer(id):
    try:
        reviewer = ControllerReviewer.get_reviewer_by_id(db, id)
        if reviewer:
            try:
                ControllerReviewer.desactivate_reviewer(db, id)
                flash("Revisor Eliminado Exitosamente...")
                return redirect(url_for("reviewer.reviewer"))
            except Exception as ex:
                raise Exception(ex)
        else:
            flash("No se pudo eliminar el Revisor...")
            return redirect(url_for("reviewer.reviewer"))
    except Exception as ex:
        raise Exception(ex)


# Upload Reviewers by csv file
@reviewer_bp.route("/upload_reviewers", methods=["POST"])
@login_required
def upload_reviewers():
    try:
        if "csv_file" not in request.files:
            flash("No file part...")
            return redirect(url_for("reviewer.create_reviewer_form"))
        csv_file = request.files["csv_file"]
        separator = request.form["Select_separator"]
        codificator = request.form["Select_codificator"]
        if csv_file.filename == "":
            flash("Sin archivo seleccionado...")
            return redirect(url_for("reviewer.create_reviewer_form"))
        if csv_file:
            data = ControllerReviewer.process_reviewer_csv(
                db, separator, codificator, csv_file
            )
            flash("Revisores Subidos Exitosamente...")
            return redirect(url_for("reviewer.create_reviewer_form"))
    except Exception as ex:
        raise Exception(ex)


# Upload Reviewers by csv file
@reviewer_bp.route("/upload_reviewer_assignations", methods=["POST"])
@login_required
def upload_reviewer_assignations():
    try:
        if "csv_file" not in request.files:
            flash("No file part...")
            return redirect(url_for("reviewer.assign_reviewer_thesis_form"))
        
        csv_file = request.files["csv_file"]
        separator = request.form["Select_separator"]
        codificator = request.form["Select_codificator"]

        if csv_file.filename == "":
            flash("Sin archivo seleccionado...")
            return redirect(url_for("reviewer.assign_reviewer_thesis_form"))
        
        if csv_file:
            data = ControllerReviewer.process_relations_csv(
                db, separator, codificator, csv_file
            )
            flash("Relaciones Subidas Exitosamente...")
            return redirect(url_for("reviewer.assign_reviewer_thesis_form"))
        
    except Exception as ex:   
        flash("Error, duplicado o campo invalido...")
        return redirect(url_for("reviewer.assign_reviewer_thesis_form"))
