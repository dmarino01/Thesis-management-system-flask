from datetime import datetime
import os
import locale
from flask import (
    Blueprint,
    make_response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from flask_login import login_required
import pandas as pd
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerRecommendation import ControllerRecommendation
from controllers.ControllerReview import ControllerReview
from controllers.ControllerReviewer import ControllerReviewer
from controllers.ControllerAdvisor import ControllerAdvisor
from werkzeug.utils import secure_filename
from xhtml2pdf import pisa
from io import BytesIO
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
        review_details = ControllerReview.get_review_details_by_thesis_id(db, id)
        status_review = ControllerReview.getStatusReview(db, id)
        template_vars = {
            "thesis": thesis,
            "recommendations": recommendations,
            "review_details": review_details,
            "status_review": status_review,
        }
        return render_template("myThesis/detail.html", **template_vars)
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
        template_vars = {
            "thesis": thesis,
            "dissertation_exists": dissertation_exists,
        }
        return render_template("myThesis/dissertation.html", **template_vars)
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
    template_vars = {
        "thesis": thesis,
        "sign_if_exists": sign_if_exists,
        "result": result,
    }
    return render_template("myThesis/sign_review.html", **template_vars)


# Save sign of thesis review
@thesis_bp.route("/save_sign/<int:id>", methods=["POST"])
@login_required
def save_sign(id):
    try:
        if "sign" in request.files:
            image_file = request.files["sign"]

            if image_file.filename == "":
                flash("Sin archivo seleccionado...", "danger")
                return redirect(url_for("thesis.sign_review_thesis_page", id=id))

            if not allowed_img(image_file.filename):
                flash(
                    "Formato invalido. Seleccione una imagen (e.g., .jpg, .png, .jpeg).",
                    "danger",
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
        flash(f"An error occurred: {ex}", "danger")
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
    units = ControllerThesis.getAllUnits(db)
    return render_template("myThesis/create.html", current_date=current_date, units=units)


@thesis_bp.route("/get_mentions")
@login_required
def get_mentions():
    unit_id = request.args.get('unit_id')
    mentions = ControllerThesis.getAllMentionsById(db, unit_id)
    mentions_data = [{'id': mention.id, 'name': mention.name} for mention in mentions]
    return jsonify({'mentions': mentions_data})


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
        turnitin_porcentaje = request.form["turnitin_porcentaje"]
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

        if title and abstract and turnitin_porcentaje:
            ControllerThesis.updateThesis(
                db,
                id,
                title,
                abstract,
                new_filename,
                new_filename_turnitin,
                turnitin_porcentaje,
            )
            flash("Tesis editada correctamente", "success")
            return redirect(url_for("thesis.myThesis", id=id))
        else:
            flash("No deben haber campos vacios...", "danger")
            return redirect(url_for("thesis.edit_thesis_form", id=id))
    except Exception as ex:
        flash(f"Error updating thesis: {str(ex)}", "danger")
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
        turnitin_porcentaje = request.form["turnitin_porcentaje"]
        project_id = request.form.get("project_id")
        expiration_date = request.form.get("expiration_date")
        mencion = request.form["mencion"]
        project_creation_date = request.form["project_creation_date"]

        if not project_id:
            project_id = 0
        else:
            project_id = int(project_id)

        if title and abstract and pdf_file and pdf_turnitin and turnitin_porcentaje and mencion:
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
                    turnitin_porcentaje,
                    expiration_date,
                    mencion,
                    project_creation_date,
                )
                return redirect(url_for("thesis.myThesis"))
            else:
                flash("Formato invalido. Seleccione un archivo PDF.", "danger")
                return redirect(url_for("thesis.myThesis"))
        else:
            flash("No deben haber campos vacios.", "danger")
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
        mencion = request.form["mencion"]
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
                    mencion,
                    project_creation_date,
                )

                return redirect(url_for("thesis.myThesis"))
            else:
                flash("Formato invalido. Seleccione un archivo PDF.", "danger")
                return redirect(url_for("thesis.myThesis"))
        else:
            flash("No deben haber campos vacios.", "danger")
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
            flash("Tesis Eliminado Exitosamente...", "success")
            return redirect(url_for("thesis.myThesis"))
        else:
            flash("No se pudo eliminar la Tesis...", "danger")
            return redirect(url_for("thesis.myThesis"))
    except Exception as ex:
        raise Exception(ex)


# Function to check if the file extension is a pdf
def allowed_pdf(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"


# Function to check if the file extension is a image
def allowed_img(filename):
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Page Thesis by Admin
@thesis_bp.route("/tesis")
@login_required
def tesis():
    data = ControllerThesis.getThesisForAdmin(db)
    return render_template("components/tesis/index.html", thesis=data)


# Page Assign Jury for Thesis by Admin
@thesis_bp.route("/admin_assigns_jury_page/<int:id>")
@login_required
def admin_assigns_jury_page(id):
    thesis = ControllerThesis.get_thesis_by_id(db, id)
    left_reviewers = ControllerReviewer.getLeftReviewersToAssign(db, id)
    assigned_reviewers = ControllerReviewer.getReviewersByThesisId(db, id)
    total_assigned_reviewer = ControllerReviewer.getTotalReviewersByThesisId(db, id)
    template_vars = {
        "thesis": thesis,
        "left_reviewers": left_reviewers,
        "assigned_reviewers": assigned_reviewers,
        "total_assigned_reviewer": total_assigned_reviewer,
    }
    return render_template("components/tesis/assign_jury.html", **template_vars)


# Page Assign Advisor for Thesis by Admin
@thesis_bp.route("/admin_assigns_advisor_page/<int:id>")
@login_required
def admin_assigns_advisor_page(id):
    thesis = ControllerThesis.get_thesis_by_id(db, id)
    left_advisors = ControllerAdvisor.getLeftAdvisorsToAssign(db, id)
    assigned_advisors = ControllerAdvisor.getAdvisorsByThesisId(db, id)
    total_assigned_advisor = ControllerAdvisor.getTotalAdvisorsByThesisId(db, id)
    template_vars = {
        "thesis": thesis,
        "left_advisors": left_advisors,
        "assigned_advisors": assigned_advisors,
        "total_assigned_advisor": total_assigned_advisor,
    }
    return render_template("components/tesis/assign_advisor.html", **template_vars)


@thesis_bp.route("/admin_generates_tesis/<int:id>")
@login_required
def generate_pdf(id):
    # Define your data
    institution_name = "UNT"
    academic_program = "Nombre del Programa Académico"
    date = "Fecha"
    thesis_title = "Título de la Tesis"
    student_name = "Nombre del Estudiante"
    
    defense_date = "Fecha de Defensa"
    defense_time = "Hora de Defensa"
    defense_location = "Lugar de Defensa"
    
    review_details = ControllerReview.get_review_details_by_thesis_id(db, id)
    signatures = ControllerReview.get_review_details_by_thesis_id(db, id)
    thesis_details = ControllerThesis.get_thesis_by_id(db, id)
    status_review = ControllerReview.getStatusReview(db, id)
    last_date = ControllerReview.getLastReviewDate(db, id)
    academic_degree = ControllerThesis.getUnitByMention(db, id)
    advisor_name = "Nombre del Asesor de Tesis"
    formatted_date = last_date.review_date.strftime('%d de %B de %Y a las %H:%M:%S')
    
    conclusions = [
        "Se considera que la tesis cumple con los requisitos establecidos para obtener el grado de " f"{academic_degree}.",
        "Los resultados presentados demuestran un conocimiento profundo del tema de investigación y un aporte significativo al campo académico.",
        "El estudiante demostró habilidades para la investigación, análisis crítico y capacidad de expresión oral."
    ]
    template_vars = {
        "institution_name":institution_name,
        "academic_program":academic_program,
        "date":date,
        "thesis_title":thesis_title,
        "student_name":student_name,
        "academic_degree":academic_degree,
        "defense_date":defense_date,
        "defense_time":defense_time,
        "defense_location":defense_location,
        "advisor_name":advisor_name,
        "review_details":review_details,
        "signatures":signatures,
        "conclusions":conclusions,
        "thesis_details":thesis_details,
        "status_review":status_review,
        "last_date":formatted_date,
    }
    # Render the HTML template
    html_content = render_template('components/tesis/acta.html', **template_vars)

    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()

    # Convert HTML to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html_content, dest=buffer)

    # Check if the conversion was successful
    if pisa_status.err:
        return "Error converting HTML to PDF"

    # Move the buffer's pointer to the beginning
    buffer.seek(0)

    # Set up the response to return the PDF
    response = make_response(buffer.read())
    response.mimetype = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=acta_defensa_tesis.pdf'

    return response