import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerRecommendation import ControllerRecommendation
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import uuid
from config import db

thesis_bp = Blueprint("thesis", __name__)
UPLOAD_FOLDER = os.path.join("src", "static", "file", "thesis")


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
        recommendations = ControllerRecommendation.get_recommendations_by_thesis_id(
            db, id
        )
        return render_template(
            "myThesis/detail.html", thesis=thesis, recommendations=recommendations
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
    return render_template("myThesis/create.html")


# Update Thesis Route
@thesis_bp.route("/update_thesis/<int:id>", methods=["POST"])
@login_required
def update_thesis(id):
    try:
        # Catch info from the forms
        title = request.form["title"]
        abstract = request.form["abstract"]
        old_pdf_link = request.form["old_pdf_link"]    
        pdf_file = request.files["pdf_file"]
        
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
             
        if title and abstract:
            ControllerThesis.updateThesis(db, id, title, abstract, new_filename)
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
        if title and abstract and pdf_file:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            if pdf_file and allowed_file(pdf_file.filename):
                # Generate a unique identifier
                unique_id = str(uuid.uuid4().hex[:8])
                # Create the unique filename
                filename = secure_filename(pdf_file.filename)
                filename_without_extension, extension = os.path.splitext(filename)
                new_filename = f"{unique_id}_{filename_without_extension}{extension}"
                # Save path and file
                pdf_path = os.path.join(UPLOAD_FOLDER, new_filename)
                pdf_file.save(pdf_path)
                ControllerThesis.createProjectThesis(db, title, abstract, new_filename)
                return redirect(url_for("thesis.myThesis"))
            else:
                flash("Invalid file format. Please upload a PDF file.")
                return redirect(url_for("thesis.create_thesis_form"))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for("thesis.create_thesis_form"))
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
