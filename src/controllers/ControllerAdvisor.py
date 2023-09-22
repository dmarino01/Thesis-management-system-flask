from models.Advisor import Advisor
from models.Person import Person
from sqlalchemy import text

class ControllerAdvisor():

    @classmethod
    def getAdvisors(cls, db):
        try:
            session = db.session()
            sql = text(
                "SELECT A.advisor_code, A.institution, A.person_id, A.advisor_id, P.firstname, P.lastname, P.phone, P.address, P.email "
                "FROM ADVISOR A INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "WHERE is_deleted = 0;"
            )
            result = session.execute(sql)
            rows=result.fetchall()
            advisors = []
            if rows != None:
                for row in rows:
                    advisor = Advisor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
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
                "SELECT A.advisor_code, A.institution, A.person_id, A.advisor_id, P.firstname, P.lastname, P.phone, P.address, P.email "
                "FROM Advisor A INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "WHERE is_deleted = 0 AND firstname "
                "LIKE :name OR lastname LIKE :name"
            )
            result = session.execute(sql, {'name': f'%{name}%'})
            rows=result.fetchall()
            advisors = []
            if rows != None:
                for row in rows:
                    advisor = Advisor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    advisors.append(advisor)
                return advisors
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    #Create a New Advisor
    @classmethod    
    def createAdvisor(cls, db, advisor_code, firstname, lastname, institution, phone, address, email):
        try:
            session = db.session()
            sql = text(
                "INSERT INTO PERSON (firstname, lastname, phone, address, email) "
                "VALUES (:firstname, :lastname, :phone, :address, :email); "
                "SET @person_id = LAST_INSERT_ID(); "
                "INSERT INTO ADVISOR (advisor_code, institution, person_id) "
                "VALUES (:advisor_code, :institution, @person_id);"
            )
            params = {
                'advisor_code': advisor_code,
                'firstname': firstname,
                'lastname': lastname,
                'institution': institution,
                'phone': phone,
                'address': address,
                'email': email               
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
                "SELECT A.advisor_code, A.institution, A.advisor_id, A.person_id, P.firstname, P.lastname, P.phone, P.address, P.email "
                "FROM ADVISOR A " 
                "INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
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
                    'phone': row[6],
                    'address': row[7],
                    'email': row[8]
                }
                return advisor
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    #Update an advisor info
    @classmethod
    def update_advisor(cls, db, id, advisor_code, firstname, lastname, institution, phone, address, email):
        try:
            session = db.session()
            sql = text(
                "UPDATE ADVISOR SET advisor_code = :advisor_code, institution = :institution WHERE advisor_id = :advisor_id; "
                "SET @person_id = (SELECT person_id FROM ADVISOR WHERE advisor_id = :advisor_id); "
                "UPDATE PERSON SET firstname = :firstname, lastname = :lastname, phone = :phone, address = :address, email = :email "
                "WHERE person_id = @person_id;"
            )
            params = {
                'advisor_id': id,
                'advisor_code': advisor_code,   
                'firstname': firstname,
                'lastname': lastname,
                'institution': institution,
                'phone': phone,
                'address': address,
                'email': email               
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