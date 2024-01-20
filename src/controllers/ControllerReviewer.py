import csv
from datetime import date, datetime
from io import StringIO
from models.Reviewer import Reviewer
from models.AssignedReviewer import AssignedReviewer
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash


class ControllerReviewer:
    @classmethod
    def getReviewers(cls, db):
        try:
            session = db.session()
            sql = text("CALL GetReviewers();")
            result = session.execute(sql)
            rows = result.fetchall()
            reviewers = []
            if rows != None:
                for row in rows:
                    reviewer = Reviewer(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9],
                        row[10],
                        row[11],
                    )
                    reviewers.append(reviewer)
                return reviewers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    # Search Reviewer
    @classmethod
    def getReviewersbyName(cls, db, name):
        try:
            session = db.session()
            sql = text("CALL GetReviewersByName(:name)")
            result = session.execute(sql, {"name": f"%{name}%"})
            rows = result.fetchall()
            reviewers = []
            if rows != None:
                for row in rows:
                    reviewer = Reviewer(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9],
                        row[10],
                        row[11],
                    )
                    reviewers.append(reviewer)
                return reviewers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    # Create a New Reviewer
    @classmethod
    def createReviewer(
        cls,
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
    ):
        try:
            hashed_password = generate_password_hash(password)
            session = db.session()
            sql = text(
                "CALL CreateReviewer(:reviewer_code, :firstname, :lastname, :dni, :grade, :phone, :address, :email, :username, :password);"
            )
            params = {
                "reviewer_code": reviewer_code,
                "firstname": firstname,
                "lastname": lastname,
                "dni": dni,
                "grade": grade,
                "phone": phone,
                "address": address,
                "email": email,
                "username": username,
                "password": hashed_password,
            }
            session.execute(sql, params)
            session.commit()
            return {"message": "Reviewer created successfully"}, 201
        except Exception as ex:
            raise Exception(ex)

    # Get Reviewer by ID
    @classmethod
    def get_reviewer_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetReviewerById(:id);")
            result = session.execute(sql, {"id": id})
            rows = result.fetchall()
            if rows:
                row = rows[0]
                reviewer = {
                    "reviewer_code": row[0],
                    "grade": row[1],
                    "reviewer_id": row[2],
                    "person_id": row[3],
                    "firstname": row[4],
                    "lastname": row[5],
                    "dni": row[6],
                    "phone": row[7],
                    "address": row[8],
                    "email": row[9],
                    "image": row[10],
                    "username": row[11],
                }
                return reviewer
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    
    # Get Reviewers by Thesis ID
    @classmethod
    def get_reviewers_by_thesis_id(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetReviewersByThesisId(:p_thesis_id);")
            result = session.execute(sql, {"p_thesis_id": id})
            rows = result.fetchall()
            reviewers = []
            if rows != None:
                for row in rows:
                    reviewer = AssignedReviewer(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                    )
                    reviewers.append(reviewer)
                return reviewers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    
    #Obtain number of reviewer by thesis id
    @classmethod
    def getTotalReviewersByThesisId(cls, db, id):
        try:
            session = db.session()    
            sql = text('CALL GetTotalReviewersByThesisId(:p_thesis_id);')
            result = session.execute(sql, {"p_thesis_id": id})
            count = result.fetchone()[0]
            result.close()
            return count
        except Exception as ex:
            raise Exception(ex)
        
    #Obtain reviewer no assigned to thesis 
    @classmethod    
    def getLeftReviewersToAssign(cls, db, id):
        try:  
            session = db.session()
            sql = text("CALL getLeftReviewersToAssign(:p_thesis_id)")
            result = session.execute(sql, {"p_thesis_id": id})
            rows = result.fetchall()
            reviewers = []
            if rows != None:
                for row in rows:
                    reviewer = Reviewer(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9],
                        row[10],
                        row[11],
                    )
                    reviewers.append(reviewer)
                return reviewers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        

    # Update an reviewer info
    @classmethod
    def update_reviewer(
        cls,
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
    ):
        try:
            session = db.session()
            sql = text(
                "CALL UpdateReviewer(:reviewer_id, :reviewer_code, :firstname, :lastname, :dni, :grade, :phone, :address, :email, :username);"
            )
            params = {
                "reviewer_id": id,
                "reviewer_code": reviewer_code,
                "firstname": firstname,
                "lastname": lastname,
                "dni": dni,
                "grade": grade,
                "phone": phone,
                "address": address,
                "email": email,
                "username": username,
            }
            session.execute(sql, params)
            session.commit()
            return {"message": "Reviewer updated successfully"}, 200

        except Exception as ex:
            raise Exception(ex)

    # Logical deletion of a reviewer
    @classmethod
    def desactivate_reviewer(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL DesactivateReviewer(:id);")
            session.execute(sql, {"id": id})
            session.commit()
            return {"message": "Reviewer created successfully"}, 200
        except Exception as ex:
            raise Exception(ex)

    # Uploading reviewers by csv file
    @classmethod
    def process_reviewer_csv(cls, db, separator, codificator, csv_file):
        try:
            lines = (
                csv_file.read().decode(f"{codificator}", errors="replace").splitlines()
            )
            with db.session() as session:
                first_line = True
                for line in lines:
                    if first_line:
                        first_line = False
                        continue
                    values = line.split(f"{separator}")
                    hashed_password = generate_password_hash(values[9])
                    sql = text(
                        "CALL CreateReviewer(:reviewer_code, :firstname, :lastname, :dni, :grade, :phone, :address, :email, :username, :password);"
                    )
                    params = {
                        "reviewer_code": values[0],
                        "firstname": values[1],
                        "lastname": values[2],
                        "dni": values[3],
                        "grade": values[4],
                        "phone": values[5],
                        "address": values[6],
                        "email": values[7],
                        "username": values[8],
                        "password": hashed_password,
                    }
                    session.execute(sql, params)
                    session.commit()
                return {"message": "Reviewers uploaded successfully"}, 200
        except Exception as ex:
            raise Exception(ex)

    # Uploading authors - reviewers relation by csv file
    @classmethod
    def process_relations_csv(cls, db, separator, codificator, csv_file):
        try:
            assignation_date = date.today().strftime("%Y-%m-%d")
            lines = (
                csv_file.read().decode(f"{codificator}", errors="replace").splitlines()
            )
            with db.session() as session:
                for line_number, line in enumerate(lines, start=1):
                    if line_number == 1:  # Skip the header line
                        continue

                    if not line.strip():  # Skip empty lines
                        continue

                    values = line.split(separator)

                    if len(values) < 3:  # Check if there are enough values
                        # Handle the case where the line doesn't have enough values
                        print(
                            f"Skipping line {line_number}: {line}. Expected at least 3 values, found {len(values)}."
                        )
                        continue

                    sql = text(
                        "CALL AssignReviewersToThesisByCodes(:reviewer_code, :thesis_id, :reviewer_role_id, :assignation_date);"
                    )
                    params = {
                        "reviewer_code": values[0],
                        "thesis_id": values[1],
                        "reviewer_role_id": values[2],
                        "assignation_date": assignation_date,
                    }
                    session.execute(sql, params)
                    session.commit()
                return {"message": "Relations uploaded successfully"}, 200

        except SQLAlchemyError as e:
            print(f"SQLAlchemyError occurred: {e}")
            return {"error": "Database error occurred"}, 500

        except Exception as e:
            print(f"Exception occurred: {e}")
            return {"error": str(e)}, 500
