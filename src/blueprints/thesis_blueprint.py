from datetime import datetime
import os
from flask import (
    Blueprint,
    make_response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import login_required
import pandas as pd
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerRecommendation import ControllerRecommendation
from controllers.ControllerReview import ControllerReview
from werkzeug.utils import secure_filename
import uuid
from config import db

thesis_bp = Blueprint("thesis", __name__)
UPLOAD_FOLDER = os.path.join("src", "static", "file", "thesis")
UPLOAD_FOLDER_TURNITIN = os.path.join("src", "static", "file", "turnitin")
UPLOAD_FOLDER_ARTICLE = os.path.join("src", "static", "file", "article")
UPLOAD_FOLDER_SIGNATURE = os.path.join("src", "static", "file", "signature")


# Thesis Index
@thesis_bp.route("/myThesis")
@login_required
def myThesis():
    project_filter = request.args.get('project_filter')
    status_filter = request.args.get('status_filter')
    data = ControllerThesis.getThesis(db, project_filter, status_filter)
    return render_template("myThesis/index.html", thesis=data)


# View Thesis Page
@thesis_bp.route("/view_thesis_page/<int:id>", methods=["GET"])
@login_required
def view_thesis_page(id):
    try:
        thesis = ControllerThesis.get_thesis_by_id(db, id)
        recommendations = ControllerRecommendation.get_recommendations_by_thesis_id(db, id)
        review_details = ControllerReview.get_review_details_by_thesis_id(db, id)
        return render_template("myThesis/detail.html", thesis=thesis, recommendations=recommendations, review_details=review_details)
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


# Sign Review Thesis Form
@thesis_bp.route("/sign_review_thesis_page/<int:id>", methods=["GET"])
@login_required
def sign_review_thesis_page(id):
    thesis = ControllerThesis.get_thesis_by_id(db, id)
    result = ControllerThesis.get_link_sign(db, id)
    sign_if_exists = ControllerThesis.get_sign_if_exists(db, id)
    return render_template("myThesis/sign_review.html", thesis=thesis, sign_if_exists=sign_if_exists, result=result)


# Save sign of thesis review
@thesis_bp.route("/save_sign/<int:id>", methods=["POST"])
@login_required
def save_sign(id):
    try:
        if "sign" in request.files:
            image_file = request.files["sign"]

            if image_file.filename == "":
                flash("Sin archivo seleccionado...")
                return redirect(url_for("thesis.sign_review_thesis_page", id=id))

            if not allowed_img(image_file.filename):
                flash(
                    "Invalid file type. Please upload an image file (e.g., .jpg, .png, .jpeg)."
                )
                return redirect(url_for("thesis.sign_review_thesis_page", id=id))

            os.makedirs(UPLOAD_FOLDER_SIGNATURE, exist_ok=True)

            # Generate a unique filename to avoid conflicts
            unique_id = str(uuid.uuid4().hex[:8])
            filename = secure_filename(image_file.filename)
            new_filename_sign = f"{unique_id}_{filename}"

            sign_path = os.path.join(UPLOAD_FOLDER_SIGNATURE, new_filename_sign)

            # Save the file to the signature folder
            image_file.save(sign_path)

            # Pass the path to the ControllerThesis function
            ControllerThesis.createSignThesis(db, new_filename_sign, id)

        return redirect(url_for("thesis.myThesis"))

    except Exception as ex:
        flash(f"An error occurred: {ex}")
        return redirect(url_for("thesis.sign_review_thesis_page", id=id))


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
            filename_turnitin_without_extension, extension = os.path.splitext(
                filename_turnitin
            )
            new_filename_turnitin = (
                f"{unique_id}_{filename_turnitin_without_extension}{extension}"
            )
            # Save path and file
            pdf_path1 = os.path.join(UPLOAD_FOLDER_TURNITIN, new_filename_turnitin)
            pdf_turnitin.save(pdf_path1)
        else:
            new_filename_turnitin = old_turnitin_link

        if title and abstract:
            ControllerThesis.updateThesis(
                db, id, title, abstract, new_filename, new_filename_turnitin
            )
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
            if allowed_pdf(pdf_file.filename) and allowed_pdf(pdf_turnitin.filename):
                # Generate a unique identifier
                unique_id = str(uuid.uuid4().hex[:8])
                # Create the unique filename
                filename_pdf = secure_filename(pdf_file.filename)
                filename_turnitin = secure_filename(pdf_turnitin.filename)

                filename_pdf_without_extension, extension = os.path.splitext(
                    filename_pdf
                )
                filename_turnitin_without_extension, extension = os.path.splitext(
                    filename_turnitin
                )

                new_filename_pdf = (
                    f"{unique_id}_{filename_pdf_without_extension}{extension}"
                )
                new_filename_turnitin = (
                    f"{unique_id}_{filename_turnitin_without_extension}{extension}"
                )
                # Save path and file
                pdf_path = os.path.join(UPLOAD_FOLDER, new_filename_pdf)
                turnitin_path = os.path.join(
                    UPLOAD_FOLDER_TURNITIN, new_filename_turnitin
                )

                pdf_file.save(pdf_path)
                pdf_turnitin.save(turnitin_path)

                ControllerThesis.createProjectThesis(
                    db,
                    title,
                    abstract,
                    project_id,
                    new_filename_pdf,
                    new_filename_turnitin,
                    expiration_date,
                    project_creation_date,
                )
                return redirect(url_for("thesis.myThesis"))
            else:
                flash("Invalid file format. Please upload a PDF file.")
                return redirect(url_for("thesis.myThesis"))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for("thesis.myThesis"))
    except Exception as ex:
        raise Exception(ex)


# Save Dissertation
@thesis_bp.route("/save_dissertation_thesis", methods=["POST"])
@login_required
def save_dissertation_thesis():
    try:
        title = request.form["title"]
        abstract = request.form["abstract"]

        pdf_file = request.files["pdf_file"]
        pdf_turnitin = request.files["pdf_turnitin"]
        pdf_article = request.files["pdf_article"]

        project_id = request.form.get("project_id")
        expiration_date = request.form.get("expiration_date")
        project_creation_date = request.form["project_creation_date"]

        if title and abstract and pdf_file and pdf_turnitin and pdf_article:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            if (
                allowed_pdf(pdf_file.filename)
                and allowed_pdf(pdf_turnitin.filename)
                and allowed_pdf(pdf_article.filename)
            ):
                # Generate a unique identifier
                unique_id = str(uuid.uuid4().hex[:8])
                # Create the unique filename
                filename_pdf = secure_filename(pdf_file.filename)
                filename_turnitin = secure_filename(pdf_turnitin.filename)
                filename_article = secure_filename(pdf_article.filename)
                # Breakdown old filename
                filename_pdf_without_extension, extension = os.path.splitext(
                    filename_pdf
                )
                filename_turnitin_without_extension, extension = os.path.splitext(
                    filename_turnitin
                )
                filename_article_without_extension, extension = os.path.splitext(
                    filename_article
                )
                # Establish new filename
                new_filename_pdf = (
                    f"{unique_id}_{filename_pdf_without_extension}{extension}"
                )
                new_filename_turnitin = (
                    f"{unique_id}_{filename_turnitin_without_extension}{extension}"
                )
                new_filename_article = (
                    f"{unique_id}_{filename_article_without_extension}{extension}"
                )
                # Save path and file
                pdf_path = os.path.join(UPLOAD_FOLDER, new_filename_pdf)
                turnitin_path = os.path.join(
                    UPLOAD_FOLDER_TURNITIN, new_filename_turnitin
                )
                article_path = os.path.join(UPLOAD_FOLDER_ARTICLE, new_filename_article)

                pdf_file.save(pdf_path)
                pdf_turnitin.save(turnitin_path)
                pdf_article.save(article_path)

                ControllerThesis.createDissertationThesis(
                    db,
                    title,
                    abstract,
                    project_id,
                    new_filename_pdf,
                    new_filename_turnitin,
                    new_filename_article,
                    expiration_date,
                    project_creation_date,
                )

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
def allowed_pdf(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"


# Report thesis without reviewers
@thesis_bp.route("/report_ptsr")
@login_required
def report_ptsr():
    try:
        total_thesis = ControllerThesis.getTotalThesis(db)
        total_thesis_without_reviewers = ControllerThesis.getTotalThesisWithoutReviewer(
            db
        )
        thesis_without_reviewers = ControllerThesis.getThesisWithoutReviewers(db)
        return render_template(
            "report/thesis_without_reviewers.html",
            total_thesis=total_thesis,
            thesis_without_reviewers=thesis_without_reviewers,
            total_thesis_without_reviewers=total_thesis_without_reviewers,
        )
    except Exception as ex:
        raise Exception(ex)


# Report thesis without reviews
@thesis_bp.route("/report_ptsc")
@login_required
def report_ptsc():
    try:
        total_thesis = ControllerThesis.getTotalThesis(db)
        total_thesis_without_reviews = ControllerThesis.getTotalThesisWithoutReviews(db)
        thesis_without_reviews = ControllerThesis.getThesisWithoutReviews(db)
        return render_template(
            "report/thesis_without_reviews.html",
            total_thesis=total_thesis,
            thesis_without_reviews=thesis_without_reviews,
            total_thesis_without_reviews=total_thesis_without_reviews,
        )
    except Exception as ex:
        raise Exception(ex)


# Report of Thesis without Reviewers AS EXCEL
@thesis_bp.route("/download_excel_tesis_sin_revisores")
@login_required
def download_excel_tesis_sin_revisores():
    try:
        thesis_without_reviewers = ControllerThesis.getThesisWithoutReviewers(db)
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(thesis_without_reviewers)
        # Convert DataFrame to Excel
        excel_file = "report.xlsx"
        df.to_excel(excel_file, index=False)
        # Send the Excel file in the response
        response = make_response(open(excel_file, "rb").read())
        response.headers["Content-Type"] = "application/vnd.ms-excel"
        response.headers["Content-Disposition"] = "attachment; filename=report.xlsx"
        return response
    except Exception as ex:
        raise Exception(ex)


# Report of Thesis without Reviews AS EXCEL
@thesis_bp.route("/download_excel_tesis_sin_revisores")
@login_required
def download_excel_tesis_sin_revisiones():
    try:
        thesis_without_reviews = ControllerThesis.getThesisWithoutReviews(db)
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(thesis_without_reviews)
        # Convert DataFrame to Excel
        excel_file = "report.xlsx"
        df.to_excel(excel_file, index=False)
        # Send the Excel file in the response
        response = make_response(open(excel_file, "rb").read())
        response.headers["Content-Type"] = "application/vnd.ms-excel"
        response.headers["Content-Disposition"] = "attachment; filename=report.xlsx"
        return response
    except Exception as ex:
        raise Exception(ex)

def allowed_img(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS