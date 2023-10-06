import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerRecommendation import ControllerRecommendation
from werkzeug.utils import secure_filename 
from config import db

thesis_bp = Blueprint('thesis', __name__)
UPLOAD_FOLDER = os.path.join("src", "static", "file", "thesis")

#Thesis Index
@thesis_bp.route('/myThesis')
@login_required
def myThesis():
    data = ControllerThesis.getThesis(db)
    return render_template("myThesis/index.html", thesis=data)

#View Thesis
@thesis_bp.route('/view_thesis_page/<int:id>', methods=['GET'])
@login_required
def view_thesis_page(id):
    thesis = ControllerThesis.get_thesis_by_id(db, id)
    
    recommendation = ControllerRecommendation.get_recommendation_by_thesis_id(db, id)
    return render_template("myThesis/detail.html", thesis=thesis, recommendation = recommendation)

#Thesis Create Form
@thesis_bp.route('/create_thesis_form')
@login_required
def create_thesis_form():
    return render_template("myThesis/create.html")

#Save Thesis Route
@thesis_bp.route('/save_thesis', methods=['POST'])
@login_required
def save_thesis():
    try:
        title = request.form['title']
        abstract = request.form['abstract']
        pdf_file = request.files['pdf_file']
        if title and abstract and pdf_file:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            if pdf_file and allowed_file(pdf_file.filename):
                filename = secure_filename(pdf_file.filename)
                pdf_path = os.path.join(UPLOAD_FOLDER, filename)
                pdf_file.save(pdf_path)
                ControllerThesis.createThesis(db, title, abstract, filename)
                return redirect(url_for('thesis.myThesis'))
            else:
                flash("Invalid file format. Please upload a PDF file.")
                return redirect(url_for('thesis.create_thesis_form'))
        else:
            flash("No deben haber campos vacios...")
            return redirect(url_for('thesis.create_thesis_form'))
    except Exception as ex:
        raise Exception(ex)
    
# Deactivate an thesis
@thesis_bp.route('/desactivate_thesis/<int:id>')
@login_required
def desactivate_thesis(id):
    try:
        thesis = ControllerThesis.get_thesis_by_id(db, id)
        if thesis:
            file_path = os.path.join(UPLOAD_FOLDER, thesis['pdf_link'])
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    print("File does not exist:", file_path)
            except Exception as e:
                print("Error deleting file:", str(e))

            ControllerThesis.desactivate_thesis(db, id)
            flash("Tesis Eliminado Exitosamente...")
            return redirect(url_for('thesis.myThesis'))
        else:
            flash("No se pudo eliminar la Tesis...")
            return redirect(url_for('thesis.myThesis'))
    except Exception as ex:
        raise Exception(ex)

# Define a function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'