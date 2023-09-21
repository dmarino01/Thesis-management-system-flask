from models.Reviewer import Reviewer
from models.Person import Person
from sqlalchemy import text

class ControllerReviewer():

    @classmethod
    def getReviewers(cls, db):
        try:
            session = db.session()
            sql = text(
                "SELECT R.reviewer_code, R.reviewer_id, R.grade, R.person_id, P.firstname, P.lastname, P.phone, P.address, P.email "
                "FROM REVIEWER R INNER JOIN PERSON P "
                "ON R.person_id = P.person_id "
                "WHERE is_deleted = 0;"
            )
            result = session.execute(sql)
            rows=result.fetchall()
            reviewers = []
            if rows != None:
                for row in rows:
                    reviewer = Reviewer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    reviewers.append(reviewer)
                return reviewers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    #Search Reviewer
    @classmethod
    def getReviewersbyName(cls, db, name):
        try:
            session = db.session()
            sql = text(
                "SELECT R.reviewer_code, R.reviewer_id, R.grade, R.person_id, P.firstname, P.lastname, P.phone, P.address, P.email "
                "FROM REVIEWER R INNER JOIN PERSON P "
                "ON R.person_id = P.person_id "
                "WHERE is_deleted = 0 AND firstname "
                "LIKE :name OR lastname LIKE :name"
            )
            result = session.execute(sql, {'name': f'%{name}%'})
            rows=result.fetchall()
            reviewers = []
            if rows != None:
                for row in rows:
                    reviewer = Reviewer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    reviewers.append(reviewer)
                return reviewers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    #Create a New Reviewer
    @classmethod    
    def createReviewer(cls, db, reviewer_code, firstname, lastname, grade, phone, address, email):
        try:
            session = db.session()
            sql = text(
                "INSERT INTO PERSON (firstname, lastname, phone, address, email) "
                "VALUES (:firstname, :lastname, :phone, :address, :email); "
                "SET @person_id = LAST_INSERT_ID(); "
                "INSERT INTO REVIEWER (reviewer_code, grade, person_id) "
                "VALUES (:reviewer_code, :grade, @person_id);"
            )
            params = {
                'reviewer_code': reviewer_code,
                'firstname': firstname,
                'lastname': lastname,
                'grade': grade,
                'phone': phone,
                'address': address,
                'email': email               
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Reviewer created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)

    #Get Reviewer by ID
    @classmethod
    def get_reviewer_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT R.reviewer_code, R.grade, R.reviewer_id, R.person_id, P.firstname, P.lastname, P.phone, P.address, P.email "
                "FROM REVIEWER R " 
                "INNER JOIN PERSON P "
                "ON R.person_id = P.person_id "
                "WHERE reviewer_id = :id"
            )
            result = session.execute(sql, {"id": id})
            row = result.fetchone()
            if row:
                reviewer = {
                    'reviewer_code': row[0],
                    'grade': row[1],
                    'reviewer_id': row[2],
                    'person_id': row[3],
                    'firstname': row[4],
                    'lastname': row[5],
                    'phone': row[6],
                    'address': row[7],
                    'email': row[8]
                }
                return reviewer
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    #Update an reviewer info
    @classmethod
    def update_reviewer(cls, db, id, reviewer_code, firstname, lastname, grade, phone, address, email):
        try:
            session = db.session()
            sql = text(
                "UPDATE REVIEWER SET reviewer_code = :reviewer_code, grade = :grade WHERE reviewer_id = :reviewer_id; "
                "SET @person_id = (SELECT person_id FROM REVIEWER WHERE reviewer_id = :reviewer_id); "
                "UPDATE PERSON SET firstname = :firstname, lastname = :lastname, phone = :phone, address = :address, email = :email "
                "WHERE person_id = @person_id;"
            )
            params = {
                'reviewer_id': id,
                'reviewer_code': reviewer_code,   
                'firstname': firstname,
                'lastname': lastname,
                'grade': grade,
                'phone': phone,
                'address': address,
                'email': email               
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Reviewer updated successfully'}, 200

        except Exception as ex:
            raise Exception(ex)
        
    #Logical deletion of a reviewer
    @classmethod    
    def desactivate_reviewer(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "UPDATE PERSON AS p "
                "INNER JOIN REVIEWER AS r "
                "ON p.person_id = r.person_id "
                "SET p.is_deleted = 1 "
                "WHERE r.reviewer_id = :id"
            )
            session.execute(sql, {"id": id})
            session.commit()
            return {'message': 'Reviewer created successfully'}, 200
        except Exception as ex:
            raise Exception(ex)