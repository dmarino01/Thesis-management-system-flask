from models.Author import Author
from sqlalchemy import text
from werkzeug.security import generate_password_hash


class ControllerAuthor():

    @classmethod
    def getAutors(cls, db):
        try:
            session = db.session()
            sql = text("CALL GetAuthors();")
            result = session.execute(sql)
            rows=result.fetchall()
            autores = []
            if rows != None:
                for row in rows:
                    autor = Author(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    autores.append(autor)
                return autores
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    #Search Author
    @classmethod    
    def getAutorsbyName(cls, db, name):
        try:
            session = db.session()
            sql = text("CALL GetAuthorsByName(:name)")
            result = session.execute(sql, {'name': f'%{name}%'})
            rows=result.fetchall()
            authors = []
            if rows != None:
                for row in rows:
                    author = Author(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    authors.append(author)
                return authors
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod    
    def createAutor(cls, db, student_code, firstname, lastname, dni, phone, address, email, username, password):
        try:
            hashed_password = generate_password_hash(password)
            session = db.session()
            sql = text("CALL CreateAuthor(:student_code, :firstname, :lastname, :dni, :phone, :address, :email, :username, :password)")
            params = {
                'student_code': student_code,
                'firstname': firstname,
                'lastname': lastname,
                'dni': dni,
                'phone': phone,
                'address': address,
                'email': email,
                'username': username,
                'password' : hashed_password
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Autor created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)
    
    #Get Author by ID
    @classmethod
    def get_autor_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetAuthorsById(:id)")
            result = session.execute(sql, {"id": id})
            rows = result.fetchall()
            if rows:
                row = rows[0]
                autor = {
                    'student_code': row[0],
                    'author_id': row[1],
                    'person_id': row[2],
                    'firstname': row[3],
                    'lastname': row[4],
                    'dni': row[5],
                    'phone': row[6],
                    'address': row[7],
                    'email': row[8],
                    'image': row[9],
                    'username': row[10]
                }
                return autor
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    #Update an author info
    @classmethod
    def update_autor(cls, db, id, student_code, firstname, lastname, dni, phone, address, email, username):
        try:
            session = db.session()
            sql = text("CALL UpdateAuthor(:author_id, :student_code, :firstname, :lastname, :dni, :phone, :address, :email, :username)")
            params = {
                'author_id': id,
                'student_code': student_code,
                'firstname': firstname,
                'lastname': lastname,
                'dni': dni,
                'phone': phone,
                'address': address,
                'email': email,
                'username' : username              
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Autor updated successfully'}, 200

        except Exception as ex:
            raise Exception(ex)
    
    #Logical deletion of an author
    @classmethod    
    def desactivate_autor(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL DesactivateAuthor(:id)")
            session.execute(sql, {"id": id})
            session.commit()
            return {'message': 'Author created successfully'}, 200
        except Exception as ex:
            raise Exception(ex)
        
    #Obtain total number of authors
    @classmethod
    def getTotalAuthors(cls, db):
        try:
            session = db.session()
            sql = text("SELECT COUNT(*) FROM AUTHOR")
            result = session.execute(sql)
            count = result.scalar()
            session.close()
            return count
        except Exception as ex:
            raise Exception(ex)
        
    #Obtain authors without an assigned advisors
    @classmethod
    def getAuthorsWithoutAdvisor(cls, db):
        try:
            session = db.session()
            sql = text('SELECT * FROM thesis_author_without_advisor_assigned_info;')
            result = session.execute(sql)
            return result
        except Exception as ex:
            raise Exception(ex)
        
    #Obtain number of authors without an assigned advisors
    @classmethod
    def getCountofAuthorsWithoutAdvisor(cls, db):
        try:
            session = db.session()    
            sql = text('SELECT COUNT(*) FROM thesis_author_without_advisor_assigned_info;')
            result = session.execute(sql)
            count = result.fetchone()[0]
            return count
        except Exception as ex:
            raise Exception(ex)
        
    #Obtain number of authors with an assigned advisors
    @classmethod
    def getCountofAuthorsWithAdvisor(cls, db):
        try:
            session = db.session()    
            sql = text('SELECT COUNT(*) FROM thesis_author_advisor_info;')
            result = session.execute(sql)
            count = result.fetchone()[0]
            return count
        except Exception as ex:
            raise Exception(ex) 
           
    #Obtain number of authors with an assigned advisors
    @classmethod
    def getAuthorsWithAdvisor(cls, db):
        try:
            session = db.session()
            sql = text('SELECT * FROM thesis_author_advisor_info;')
            result = session.execute(sql)
            session.close()
            return result
        except Exception as ex:
            raise Exception(ex)

        
    #Uploading authors by csv file
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
                    hashed_password = generate_password_hash(values[8])
                    sql = text("CALL CreateAuthor(:student_code, :firstname, :lastname, :dni, :phone, :address, :email, :username, :password)")                 
                    params = {
                        'student_code': values[0],
                        'firstname': values[1],
                        'lastname': values[2],
                        'dni': values[3],
                        'phone': values[4],
                        'address': values[5],
                        'email': values[6],
                        'username': values[7],
                        'password' : hashed_password
                    }
                    session.execute(sql, params)
                    session.commit()
                return {'message': 'Authors uploaded successfully'}, 200                 
        except Exception as ex:
            raise Exception(ex)