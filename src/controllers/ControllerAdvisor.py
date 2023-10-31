from models.Advisor import Advisor
from sqlalchemy import text
from werkzeug.security import generate_password_hash

class ControllerAdvisor():

    @classmethod
    def getAdvisors(cls, db):
        try:
            session = db.session()
            sql = text("CALL GetAllAdvisors()")
            result = session.execute(sql)
            rows=result.fetchall()
            advisors = []
            if rows != None:
                for row in rows:
                    advisor = Advisor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                    advisors.append(advisor)
                return advisors
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_advisor_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetAdvisorById(:id)")
            result = session.execute(sql, {"id": id})
            rows = result.fetchall()
            if rows:
                row = rows[0]
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
                    'image': row[10],
                    'username': row[11]
                }
                return advisor
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getAdvisorsbyName(cls, db, name):
        try:
            session = db.session()
            sql = text("CALL GetAdvisorsByName(:name)")
            result = session.execute(sql, {'name': f'%{name}%'})
            rows=result.fetchall()
            advisors = []
            if rows != None:
                for row in rows:
                    advisor = Advisor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
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
            sql = text("CALL CreateAdvisor(:advisor_code, :firstname, :lastname, :dni, :institution, :phone, :address, :email, :username, :password)")
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
        
    #Update an advisor info
    @classmethod
    def update_advisor(cls, db, id, advisor_code, firstname, lastname, dni, institution, phone, address, email, username):
        try:
            session = db.session()
            sql = text("CALL UpdateAdvisor(:advisor_id, :advisor_code, :firstname, :lastname, :dni, :institution, :phone, :address, :email, :username)")
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
            sql = text("CALL DesactivateAdvisor(:person_id)")
            session.execute(sql, {"person_id": id})
            session.commit()
            return {'message': 'Advisor created successfully'}, 200
        except Exception as ex:
            raise Exception(ex)
        
    #Uploading advisor by csv file
    @classmethod
    def process_csv(cls, db, separator, codificator, csv_file):
        try:
            lines = csv_file.read().decode(f'{codificator}', errors='replace').splitlines()
            with db.session() as session:
                first_line = True
                for line in lines:
                    if first_line:
                        first_line = False
                        continue
                    values = line.split(f'{separator}')
                    hashed_password = generate_password_hash(values[9])
                    sql = text("CALL CreateAdvisor(:advisor_code, :firstname, :lastname, :dni, :institution, :phone, :address, :email, :username, :password)")               
                    params = {
                        'advisor_code': values[0],
                        'firstname': values[1],
                        'lastname': values[2],
                        'dni': values[3],
                        'institution': values[4],
                        'phone': values[5],
                        'address': values[6],
                        'email': values[7],
                        'username': values[8],
                        'password' : hashed_password
                    }
                    session.execute(sql, params)
                    session.commit()
                return {'message': 'Advisors uploaded successfully'}, 200                 
        except Exception as ex:
            raise Exception(ex)