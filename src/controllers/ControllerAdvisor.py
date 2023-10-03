from models.Advisor import Advisor
from sqlalchemy import text
from werkzeug.security import generate_password_hash

class ControllerAdvisor():

    @classmethod
    def getAdvisors(cls, db):
        try:
            session = db.session()
            sql = text(
                "SELECT A.advisor_code, A.institution, A.person_id, A.advisor_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM ADVISOR A INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE is_deleted = 0;"
            )
            result = session.execute(sql)
            rows=result.fetchall()
            advisors = []
            if rows != None:
                for row in rows:
                    advisor = Advisor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    advisors.append(advisor)
                return advisors
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    #Search Advisor
    @classmethod
    def getAdvisorsbyName(cls, db, name):
        try:
            session = db.session()
            sql = text(
                "SELECT A.advisor_code, A.institution, A.person_id, A.advisor_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM Advisor A INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE is_deleted = 0 "
                "AND P.firstname LIKE :name OR P.lastname LIKE :name"
            )
            result = session.execute(sql, {'name': f'%{name}%'})
            rows=result.fetchall()
            advisors = []
            if rows != None:
                for row in rows:
                    advisor = Advisor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    advisors.append(advisor)
                return advisors
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    #Create a New Advisor
    @classmethod    
    def createAdvisor(cls, db, advisor_code, firstname, lastname, dni, institution, phone, address, email, username, password):
        try:
            hashed_password = generate_password_hash(password)
            session = db.session()
            sql = text(
                "INSERT INTO PERSON (firstname, lastname, dni, phone, address, email) "
                "VALUES (:firstname, :lastname, :dni, :phone, :address, :email); "
                "SET @person_id = LAST_INSERT_ID(); "
                "INSERT INTO ADVISOR (advisor_code, institution, person_id) "
                "VALUES (:advisor_code, :institution, @person_id);"
                "INSERT INTO USER (username, password, person_id) "
                "VALUES (:username, :password, @person_id); "
                "SET @user_id = LAST_INSERT_ID(); "
                "INSERT INTO ROLE_USER (user_id, role_id) "
                "VALUES (@user_id, 4);"
            )
            params = {
                'advisor_code': advisor_code,
                'firstname': firstname,
                'lastname': lastname,
                'dni': dni,
                'institution': institution,
                'phone': phone,
                'address': address,
                'email': email,
                'username': username,
                'password': hashed_password             
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Advisor created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)
        
    
    #Get Advisor by ID
    @classmethod
    def get_advisor_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT A.advisor_code, A.institution, A.advisor_id, A.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM ADVISOR A " 
                "INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE advisor_id = :id"
            )
            result = session.execute(sql, {"id": id})
            row = result.fetchone()
            if row:
                advisor = {
                    'advisor_code': row[0],
                    'institution': row[1],
                    'advisor_id': row[2],
                    'person_id': row[3],
                    'firstname': row[4],
                    'lastname': row[5],
                    'dni': row[6],
                    'phone': row[7],
                    'address': row[8],
                    'email': row[9],
                    'username': row[10],
                }
                return advisor
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    #Update an advisor info
    @classmethod
    def update_advisor(cls, db, id, advisor_code, firstname, lastname, dni, institution, phone, address, email, username):
        try:
            session = db.session()
            sql = text(
                "UPDATE ADVISOR SET advisor_code = :advisor_code, institution = :institution WHERE advisor_id = :advisor_id; "
                "SET @person_id = (SELECT person_id FROM ADVISOR WHERE advisor_id = :advisor_id); "
                "UPDATE PERSON SET firstname = :firstname, lastname = :lastname, dni = :dni, phone = :phone, address = :address, email = :email "
                "WHERE person_id = @person_id; "
                "UPDATE USER SET username = :username "
                "WHERE person_id = @person_id; "
            )
            params = {
                'advisor_id': id,
                'advisor_code': advisor_code,
                'firstname': firstname,
                'lastname': lastname,
                'dni': dni,
                'institution': institution,
                'phone': phone,
                'address': address,
                'email': email,
                'username': username
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Advisor updated successfully'}, 200

        except Exception as ex:
            raise Exception(ex)
        
    #Logical deletion of a advisor
    @classmethod    
    def desactivate_advisor(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "UPDATE PERSON AS p "
                "INNER JOIN ADVISOR AS A "
                "ON p.person_id = a.person_id "
                "SET p.is_deleted = 1 "
                "WHERE a.advisor_id = :id"
            )
            session.execute(sql, {"id": id})
            session.commit()
            return {'message': 'Advisor created successfully'}, 200
        except Exception as ex:
            raise Exception(ex)
        
    #Get Advisor by person_id
    @classmethod
    def get_advisor_by_person_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT A.advisor_code, A.institution, A.advisor_id, A.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM ADVISOR A " 
                "INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE A.person_id = :id"
            )
            result = session.execute(sql, {"id": id})
            row = result.fetchone()
            if row:
                advisor = {
                    'advisor_code': row[0],
                    'institution': row[1],
                    'advisor_id': row[2],
                    'person_id': row[3],
                    'firstname': row[4],
                    'lastname': row[5],
                    'dni': row[6],
                    'phone': row[7],
                    'address': row[8],
                    'email': row[9],
                    'username': row[10],
                }
                return advisor
            else:
                return None
        except Exception as ex:
            raise Exception(ex)