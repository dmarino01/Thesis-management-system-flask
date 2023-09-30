from models.Reviewer import Reviewer
from sqlalchemy import text
from werkzeug.security import generate_password_hash

class ControllerReviewer():

    @classmethod
    def getReviewers(cls, db):
        try:
            session = db.session()
            sql = text(
                "SELECT R.reviewer_code, R.reviewer_id, R.grade, R.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM REVIEWER R "
                "INNER JOIN PERSON P "
                "ON R.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE is_deleted = 0;"
            )
            result = session.execute(sql)
            rows=result.fetchall()
            reviewers = []
            if rows != None:
                for row in rows:
                    reviewer = Reviewer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
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
                "SELECT R.reviewer_code, R.reviewer_id, R.grade, R.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM REVIEWER R "
                "INNER JOIN PERSON P "
                "ON R.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE is_deleted = 0 "
                "AND P.firstname LIKE :name OR P.lastname LIKE :name"
            )
            result = session.execute(sql, {'name': f'%{name}%'})
            rows=result.fetchall()
            reviewers = []
            if rows != None:
                for row in rows:
                    reviewer = Reviewer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    reviewers.append(reviewer)
                return reviewers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    #Create a New Reviewer
    @classmethod    
    def createReviewer(cls, db, reviewer_code, firstname, lastname, dni, grade, phone, address, email, username, password):
        try:
            hashed_password = generate_password_hash(password)
            session = db.session()
            sql = text(
                "INSERT INTO PERSON (firstname, lastname, dni, phone, address, email) "
                "VALUES (:firstname, :lastname, :dni, :phone, :address, :email); "
                "SET @person_id = LAST_INSERT_ID(); "
                "INSERT INTO REVIEWER (reviewer_code, grade, person_id) "
                "VALUES (:reviewer_code, :grade, @person_id);"
                "INSERT INTO USER (username, password, person_id) "
                "VALUES (:username, :password, @person_id); "
                "SET @user_id = LAST_INSERT_ID(); "
                "INSERT INTO ROLE_USER (user_id, role_id) "
                "VALUES (@user_id, 3);"
            )
            params = {
                'reviewer_code': reviewer_code,
                'firstname': firstname,
                'lastname': lastname,
                'dni': dni,
                'grade': grade,
                'phone': phone,
                'address': address,
                'email': email,
                'username': username,
                'password': hashed_password
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
                "SELECT R.reviewer_code, R.grade, R.reviewer_id, R.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM REVIEWER R " 
                "INNER JOIN PERSON P "
                "ON R.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
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
                    'dni': row[6],
                    'phone': row[7],
                    'address': row[8],
                    'email': row[9],
                    'username': row[10]
                }
                return reviewer
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    #Update an reviewer info
    @classmethod
    def update_reviewer(cls, db, id, reviewer_code, firstname, lastname, dni, grade, phone, address, email, username):
        try:
            session = db.session()
            sql = text(
                "UPDATE REVIEWER SET reviewer_code = :reviewer_code, grade = :grade WHERE reviewer_id = :reviewer_id; "
                "SET @person_id = (SELECT person_id FROM REVIEWER WHERE reviewer_id = :reviewer_id); "
                "UPDATE PERSON SET firstname = :firstname, lastname = :lastname, dni = :dni, phone = :phone, address = :address, email = :email "
                "WHERE person_id = @person_id;"
                "UPDATE USER SET username = :username "
                "WHERE person_id = @person_id; "
            )
            params = {
                'reviewer_id': id,
                'reviewer_code': reviewer_code,
                'firstname': firstname,
                'lastname': lastname,
                'dni': dni,
                'grade': grade,
                'phone': phone,
                'address': address,
                'email': email,
                'username': username,
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