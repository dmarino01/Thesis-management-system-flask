from datetime import datetime
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerRecommendation import ControllerRecommendation
from werkzeug.utils import secure_filename
import uuid
from config import db

thesis_bp = Blueprint("thesis", __name__)
UPLOAD_FOLDER = os.path.join("src", "static", "file", "thesis")
UPLOAD_FOLDER_TURNITIN = os.path.join("src", "static", "file", "turnitin")

# Thesis Index
@thesis_bp.route("/myThesis")
@login_required
def myThesis():
    data = ControllerThesis.getThesis(db)
    return render_template("myThesis/index.html", thesis=data)


# View Thesis Page
@thesis_bp.route("/view_thesis_page/<int:id>", methods=["GET"])
@login_required
def view_thesis_page(id):
    try:
        thesis = ControllerThesis.get_thesis_by_id(db, id)
        recommendations = ControllerRecommendation.get_recommendations_by_thesis_id(db, id)
        return render_template(
            "myThesis/detail.html", thesis=thesis, recommendations=recommendations
        )
    except Exception as ex:
        print(f"Error: {ex}")
        raise Exception(ex)


# View Thesis Dissertation Thesis Page
@thesis_bp.route("/view_dissertation_page/<int:id>", methods=["GET"])
@login_required
def view_dissertation_page(id):
    try:
        thesis = ControllerThesis.get_thesis_by_id(db, id)
        dissertation_exists = ControllerThesis.check_dissertation_exists(db, id)
        return render_template(
            "myThesis/dissertation.html",
            thesis=thesis,
            dissertation_exists=dissertation_exists,
        )
    except Exception as ex:
        print(f"Error: {ex}")
        raise Exception(ex)


# Edit Thesis Form
@thesis_bp.route("/edit_thesis_form/<int:id>", methods=["GET"])
@login_required
def edit_thesis_form(id):
    thesis = ControllerThesis.get_thesis_by_id(db, id)
    return render_template("myThesis/edit.html", thesis=thesis)


# Thesis Create Form
@thesis_bp.route("/create_thesis_form")
@login_required
def create_thesis_form():
    current_date = datetime.now().date()
    return render_template("myThesis/create.html", current_date=current_date)


# Update Thesis Route
@thesis_bp.route("/update_thesis/<int:id>", methods=["POST"])
@login_required
def update_thesis(id):
    try:
        # Catch info from the forms
        title = request.form["title"]
        abstract = request.form["abstract"]
        old_pdf_link = request.form["old_pdf_link"]
        old_turnitin_link = request.form["old_turnitin_link"]
        pdf_file = request.files["pdf_file"]
        pdf_turnitin = request.files["pdf_turnitin"]
        project_creation_date = request.form["project_creation_date"]

        if pdf_file and pdf_file.filename != "":
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # Delete old pdf
            file_path = os.path.join(UPLOAD_FOLDER, old_pdf_link)
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print("File does not exist:", file_path)
            # Generate a unique identifier
            unique_id = str(uuid.uuid4().hex[:8])
            # Create the unique filename
            filename = secure_filename(pdf_file.filename)
            filename_without_extension, extension = os.path.splitext(filename)
            new_filename = f"{unique_id}_{filename_without_extension}{extension}"
            # Save path and file
            pdf_path = os.path.join(UPLOAD_FOLDER, new_filename)
            pdf_file.save(pdf_path)
        else:
            new_filename = old_pdf_link

        if pdf_turnitin and pdf_turnitin.filename != "":
            os.makedirs(UPLOAD_FOLDER_TURNITIN, exist_ok=True)
            # Delete old pdf
            file_path1 = os.path.join(UPLOAD_FOLDER_TURNITIN, old_turnitin_link)
            if os.path.exists(file_path1):
                os.remove(file_path1)
            else:
                print("File does not exist:", file_path1)
            # Generate a unique identifier
            unique_id = str(uuid.uuid4().hex[:8])
            # Create the unique filename
            filename_turnitin = secure_filename(pdf_turnitin.filename)
            filename_turnitin_without_extension, extension = os.path.splitext(filename_turnitin)
            new_filename_turnitin = f"{unique_id}_{filename_turnitin_without_extension}{extension}"
            # Save path and file
            pdf_path1 = os.path.join(UPLOAD_FOLDER_TURNITIN, new_filename_turnitin)
            pdf_turnitin.save(pdf_path1)
        else:
            new_filename_turnitin = old_turnitin_link

        if title and abstract:
            ControllerThesis.updateThesis(db, id, title, abstract, new_filename, new_filename_turnitin)
            return redirect(url_for("thesis.edit_thesis_form", id=id))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for("thesis.edit_thesis_form", id=id))
    except Exception as ex:
        flash(f"Error updating thesis: {str(ex)}")
        return redirect(url_for("thesis.edit_thesis_form", id=id))


# Save Thesis Project Route
@thesis_bp.route("/save_thesis", methods=["POST"])
@login_required
def save_thesis():
    try:
        title = request.form["title"]
        abstract = request.form["abstract"]
        pdf_file = request.files["pdf_file"]
        pdf_turnitin = request.files["pdf_turnitin"]
        project_id = request.form.get("project_id")
        expiration_date = request.form.get("expiration_date")
        project_creation_date = request.form["project_creation_date"]

        if not project_id:
            project_id = 0
        else:
            project_id = int(project_id)

        if title and abstract and pdf_file and pdf_turnitin:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            if allowed_file(pdf_file.filename) and allowed_file(pdf_turnitin.filename):
                # Generate a unique identifier
                unique_id = str(uuid.uuid4().hex[:8])
                # Create the unique filename
                filename_pdf = secure_filename(pdf_file.filename)
                filename_turnitin = secure_filename(pdf_turnitin.filename)

                filename_pdf_without_extension, extension = os.path.splitext(filename_pdf)
                filename_turnitin_without_extension, extension = os.path.splitext(filename_turnitin)

                new_filename_pdf = f"{unique_id}_{filename_pdf_without_extension}{extension}"
                new_filename_turnitin = f"{unique_id}_{filename_turnitin_without_extension}{extension}"
                # Save path and file
                pdf_path = os.path.join(UPLOAD_FOLDER, new_filename_pdf)
                turnitin_path = os.path.join(UPLOAD_FOLDER_TURNITIN, new_filename_turnitin)

                pdf_file.save(pdf_path)
                pdf_turnitin.save(turnitin_path)

                ControllerThesis.createProjectThesis(db, title, abstract, project_id, new_filename_pdf, new_filename_turnitin, expiration_date, project_creation_date)
                return redirect(url_for("thesis.myThesis"))
            else:
                flash("Invalid file format. Please upload a PDF file.")
                return redirect(url_for("thesis.myThesis"))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for("thesis.myThesis"))
    except Exception as ex:
        raise Exception(ex)


# Deactivate an thesis
@thesis_bp.route("/desactivate_thesis/<int:id>")
@login_required
def desactivate_thesis(id):
    try:
        thesis = ControllerThesis.get_thesis_by_id(db, id)
        if thesis:
            file_path = os.path.join(UPLOAD_FOLDER, thesis["pdf_link"])
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    print("File does not exist:", file_path)
            except Exception as e:
                print("Error deleting file:", str(e))

            ControllerThesis.desactivate_thesis(db, id)
            flash("Tesis Eliminado Exitosamente...")
            return redirect(url_for("thesis.myThesis"))
        else:
            flash("No se pudo eliminar la Tesis...")
            return redirect(url_for("thesis.myThesis"))
    except Exception as ex:
        raise Exception(ex)


# Define a function to check if the file extension is allowed
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"
