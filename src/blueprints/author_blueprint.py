from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from controllers.ControllerAuthor import ControllerAuthor
from flask_login import login_required

from config import db

author_bp = Blueprint("author", __name__)


# Author Index
@author_bp.route("/autor")
@login_required
def autor():
    data = ControllerAuthor.getAutors(db)
    return render_template("components/autor/index.html", autores=data)


# Search for authors by name
@author_bp.route("/search_autores", methods=["POST"])
@login_required
def search_autores():
    try:
        name = request.form["keyname"]
        data = ControllerAuthor.getAutorsbyName(db, name)
        return render_template("components/autor/resultado.html", filtered_autores=data)
    except Exception as ex:
        raise Exception(ex)


# Display the create author form
@author_bp.route("/create_autor_form", methods=["GET"])
@login_required
def create_autor_form():
    return render_template("components/autor/create.html")


# Save a new author
@author_bp.route("/save_autor", methods=["POST"])
@login_required
def save_autor():
    try:
        student_code = request.form["student_code"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dni = request.form["dni"]
        phone = request.form["phone"]
        address = request.form["address"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        verify_password = request.form["verify_password"]
        if (
            student_code != ""
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
                ControllerAuthor.createAutor(
                    db,
                    student_code,
                    firstname,
                    lastname,
                    dni,
                    phone,
                    address,
                    email,
                    username,
                    password,
                )
                flash("Autor Creado Exitosamente...", "successs")
                return redirect(url_for("author.autor"))
            else:
                flash("Las contraseñas no coinciden...", "danger")
                return redirect(url_for("author.create_autor_form"))
        else:
            flash("No deben haber campos vacios...", "danger")
            return redirect(url_for("author.create_autor_form"))
    except Exception as ex:
        return redirect(url_for("author.create_autor_form"))


# Display the edit author form
@author_bp.route("/edit_autor_form/<int:id>", methods=["GET"])
@login_required
def edit_autor_form(id):
    autor = ControllerAuthor.get_autor_by_id(db, id)
    return render_template("components/autor/edit.html", autor=autor)


# Update an author
@author_bp.route("/update_autor/<int:id>", methods=["POST"])
@login_required
def update_autor(id):
    try:
        student_code = request.form["student_code"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dni = request.form["dni"]
        phone = request.form["phone"]
        address = request.form["address"]
        email = request.form["email"]
        username = request.form["username"]
        if (
            student_code != ""
            and firstname != ""
            and lastname != ""
            and dni != ""
            and phone != ""
            and email != ""
            and username != ""
        ):
            ControllerAuthor.update_autor(
                db,
                id,
                student_code,
                firstname,
                lastname,
                dni,
                phone,
                address,
                email,
                username,
            )
            flash("Autor Actualizado Exitosamente...", "success")
            return redirect(url_for("author.autor"))
        else:
            flash("No deben haber campos vacios...", "danger")
            return redirect(url_for("author.autor"))
    except Exception as ex:
        return redirect(url_for("author.edit_autor_form", id=id))


# Deactivate an author
@author_bp.route("/desactivate_autor/<int:id>")
@login_required
def desactivate_autor(id):
    try:
        autor = ControllerAuthor.get_autor_by_id(db, id)
        if autor:
            ControllerAuthor.desactivate_autor(db, id)
            flash("Autor Eliminado Exitosamente...", "success")
            return redirect(url_for("author.autor"))
        else:
            flash("No se pudo eliminar el Autor...", "danger")
            return redirect(url_for("author.autor"))
    except Exception as ex:
        raise Exception(ex)


# Upload Authors by csv file
@author_bp.route("/upload_autores", methods=["POST"])
@login_required
def upload_autores():
    try:
        if "csv_file" not in request.files:
            flash("No file part...")
            return redirect(url_for("author.create_autor_form"))
        csv_file = request.files["csv_file"]
        separator = request.form["Select_separator"]
        codificator = request.form["Select_codificator"]
        if csv_file.filename == "":
            flash("Sin archivo seleccionado...", "danger")
            return redirect(url_for("author.create_autor_form"))
        if csv_file:
            data = ControllerAuthor.process_csv(db, separator, codificator, csv_file)
            flash("Autores Subidos Exitosamente...", "danger")
            return redirect(url_for("author.create_autor_form"))
    except Exception as ex:
        raise Exception(ex)



