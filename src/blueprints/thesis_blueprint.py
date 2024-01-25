from datetime import datetime
import os
from flask import (
    Blueprint,
    make_response,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from reportlab.pdfgen import canvas
from flask_login import login_required
import pandas as pd
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerRecommendation import ControllerRecommendation
from controllers.ControllerReview import ControllerReview
from controllers.ControllerReviewer import ControllerReviewer
from controllers.ControllerAdvisor import ControllerAdvisor
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
    project_filter = request.args.get("project_filter")
    status_filter = request.args.get("status_filter")
    data = ControllerThesis.getThesis(db, project_filter, status_filter)
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
        project_creation_date = request.form["project_creation_date"]

        if not project_id:
            project_id = 0
        else:
            project_id = int(project_id)

        if title and abstract and pdf_file and pdf_turnitin and turnitin_porcentaje:
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
        template_vars = {
            "total_thesis": total_thesis,
            "thesis_without_reviewers": thesis_without_reviewers,
            "total_thesis_without_reviewers": total_thesis_without_reviewers,
        }
        return render_template("report/thesis_without_reviewers.html", **template_vars)
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
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Page Thesis by Admin
@thesis_bp.route("/tesis")
@login_required
def tesis():
    project_filter = request.args.get("project_filter")
    status_filter = request.args.get("status_filter")
    data = ControllerThesis.getThesisForAdmin(db, project_filter, status_filter)
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


@thesis_bp.route("/admin_generates_tesis")
@login_required
def generate_pdf():
    # Create a BytesIO buffer to store the PDF
    from io import BytesIO
    buffer = BytesIO()

    # Create the PDF object, using BytesIO as its "file"
    p = canvas.Canvas(buffer)

    # Add content to the PDF
    institution_name = "UNT"
    academic_program = "[Nombre del Programa Académico]"
    date = "[Fecha]"
    thesis_title = "[Título de la Tesis]"
    student_name = "[Nombre del Estudiante]"
    academic_degree = "[Grado Académico]"
    defense_date = "[Fecha de Defensa]"
    defense_time = "[Hora de Defensa]"
    defense_location = "[Lugar de Defensa]"
    evaluators = [
        ("[Nombre del Primer Evaluador]", "[Cargo del Primer Evaluador]"),
        ("[Nombre del Segundo Evaluador]", "[Cargo del Segundo Evaluador]"),
        ("[Nombre del Tercer Evaluador]", "[Cargo del Tercer Evaluador]")
    ]
    advisor_name = "[Nombre del Asesor de Tesis]"

    p.setFont("Helvetica", 12)
    p.drawCentredString(300, 750, institution_name)
    p.drawCentredString(300, 730, academic_program)
    p.drawCentredString(300, 710, date)

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 670, "ACTA DE DEFENSA DE TESIS")

    p.setFont("Helvetica", 12)
    p.drawString(50, 640, f"En {institution_name}, se llevó a cabo la defensa de la tesis titulada '{thesis_title}',")
    p.drawString(50, 625, f"presentada por el estudiante {student_name}, con el fin de obtener el grado de {academic_degree} en {academic_program}.")

    p.drawString(50, 590, f"La defensa se llevó a cabo el {defense_date} a las {defense_time} en {defense_location}.")
    p.drawString(50, 575, "El tribunal evaluador estuvo conformado por los siguientes miembros:")

    y_position = 555
    for evaluator in evaluators:
        p.drawString(50, y_position, f"{evaluator[0]}, {evaluator[1]}")
        y_position -= 15

    p.drawString(50, 510, "El estudiante presentó de manera oral y escrita los resultados de su investigación,")
    p.drawString(50, 495, "exponiendo los objetivos, metodología, resultados obtenidos y conclusiones de la tesis.")
    p.drawString(50, 480, "Posteriormente, los miembros del tribunal realizaron preguntas y comentarios,")
    p.drawString(50, 465, "generando un intercambio constructivo que permitió evaluar la calidad y profundidad del trabajo realizado.")

    p.drawString(50, 430, "Luego de la exposición y la deliberación del tribunal, se llegó a las siguientes conclusiones:")

    conclusions = [
        "1. Se considera que la tesis cumple con los requisitos establecidos para obtener el grado de.",
        f"   {academic_degree}.",
        "2. Los resultados presentados demuestran un conocimiento profundo del tema de investigación y",
        "   muestran un aporte significativo al campo académico.",
        "3. El estudiante demostró habilidades para la investigación, análisis crítico y capacidad de expresión oral."
    ]

    y_position = 410
    for conclusion in conclusions:
        p.drawString(50, y_position, conclusion)
        y_position -= 15

    p.drawString(50, 365, f"En base a lo anterior, se recomienda otorgar el grado de {academic_degree} al estudiante {student_name}.")

    p.drawString(50, 330, "El acta queda firmada por los miembros del tribunal:")

    signatures = [
        ("[Firma y Nombre del Primer Evaluador]", ""),
        ("[Firma y Nombre del Segundo Evaluador]", ""),
        ("[Firma y Nombre del Tercer Evaluador]", ""),
        ("[Firma y Nombre del Estudiante]", ""),
        ("[Firma y Nombre del Asesor de Tesis]", "")
    ]

    y_position = 310
    for signature in signatures:
        p.drawString(50, y_position, signature[0])
        y_position -= 15

    p.drawString(50, 260, "Fecha: _________")

    # Save the PDF to the buffer
    p.showPage()
    p.save()

    # Move the buffer's pointer to the beginning
    buffer.seek(0)

    # Set up the response to return the PDF
    response = make_response(buffer.read())
    response.mimetype = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=acta_defensa_tesis.pdf'

    return response

