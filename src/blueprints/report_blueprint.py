import datetime
from flask import Blueprint, make_response, render_template, request, redirect, url_for, flash
import pandas as pd
#from controllers.ControllerReport import ControllerReport
from controllers.ControllerThesis import ControllerThesis
from controllers.ControllerAuthor import ControllerAuthor
from flask_login import current_user, login_required

from config import db

report_bp = Blueprint('report', __name__)



# Report of Authors without Advisors
@report_bp.route("/report_asa")
@login_required
def report_asa():
    try:
        total_autores = ControllerAuthor.getTotalAuthors(db)
        autores_sin_asesores = ControllerAuthor.getAuthorsWithoutAdvisor(db)
        count_autores_sin_asesores = ControllerAuthor.getCountofAuthorsWithoutAdvisor(
            db
        )

        # autores_con_asesores = ControllerAuthor.getAuthorsWithAdvisor(db)
        return render_template(
            "report/authors_without_advisors.html",
            total_autores=total_autores,
            autores_sin_asesores=autores_sin_asesores,
            count_autores_sin_asesores=count_autores_sin_asesores,
            #    autores_con_asesores=autores_con_asesores,
        )
    except Exception as ex:
        raise Exception(ex)


# Report of Authors with Advisors
@report_bp.route("/report_aca")
@login_required
def report_aca():
    try:
        total_autores = ControllerAuthor.getTotalAuthors(db)
        autores_con_asesores = ControllerAuthor.getAuthorsWithAdvisor(db)
        count_autores_con_asesores = ControllerAuthor.getCountofAuthorsWithAdvisor(db)
        count_autores_sin_asesores = ControllerAuthor.getCountofAuthorsWithoutAdvisor(
            db
        )
        template_vars = {
            "total_autores": total_autores,
            "autores_con_asesores": autores_con_asesores,
            "count_autores_con_asesores": count_autores_con_asesores,
            "count_autores_sin_asesores": count_autores_sin_asesores,
        }
        return render_template("report/authors_with_advisors.html", **template_vars)
    except Exception as ex:
        raise Exception(ex)



# Report thesis without reviewers
@report_bp.route("/report_ptsr")
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
@report_bp.route("/report_ptsc")
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
@report_bp.route("/download_excel_tesis_sin_revisores")
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
@report_bp.route("/download_excel_tesis_sin_revisiones")
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
    


# Report of Authors without Advisors AS EXCEL
@report_bp.route("/download_excel_autores_sin_asesores")
@login_required
def download_excel_autores_sin_asesores():
    try:
        autores_sin_asesores = ControllerAuthor.getAuthorsWithoutAdvisor(db)
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(autores_sin_asesores)
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


# Report of Authors with Advisors AS EXCEL
@report_bp.route("/download_excel_autores_con_asesores")
@login_required
def download_excel_autores_con_asesores():
    try:
        autores_con_asesores = ControllerAuthor.getAuthorsWithAdvisor(db)
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(autores_con_asesores)
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