from models.Author import Author
from models.Person import Person
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

class ControllerAuthor():

    @classmethod
    def getAutors(cls, db):
        try:
            session = db.session()
            sql = text(
                "SELECT A.student_code, A.author_id, A.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM AUTHOR A "
                "INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE is_deleted = 0;"
            )
            result = session.execute(sql)
            rows=result.fetchall()
            autores = []
            if rows != None:
                for row in rows:
                    autor = Author(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                    autores.append(autor)
                return autores
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod    
    def getAutorsbyName(cls, db, name):
        try:
            session = db.session()
            sql = text(
                "SELECT A.student_code, A.author_id, A.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM AUTHOR A "
                "INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE is_deleted = 0 "
                "AND P.firstname LIKE :name OR P.lastname LIKE :name"
            )
            result = session.execute(sql, {'name': f'%{name}%'})
            rows=result.fetchall()
            autores = []
            if rows != None:
                for row in rows:
                    autor = Author(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                    autores.append(autor)
                return autores
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod    
    def createAutor(cls, db, student_code, firstname, lastname, dni, phone, address, email, username, password):
        try:
            hashed_password = generate_password_hash(password)
            session = db.session()
            sql = text(
                "INSERT INTO PERSON (firstname, lastname, dni, phone, address, email) "
                "VALUES (:firstname, :lastname, :dni, :phone, :address, :email); "
                "SET @person_id = LAST_INSERT_ID(); "
                "INSERT INTO AUTHOR (student_code, person_id) "
                "VALUES (:student_code, @person_id); "
                "INSERT INTO USER (username, password, person_id) "
                "VALUES (:username, :password, @person_id); "
                "SET @user_id = LAST_INSERT_ID(); "
                "INSERT INTO ROLE_USER (user_id, role_id) "
                "VALUES (@user_id, 2);"
            )
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
            sql = text(
                "SELECT A.student_code, A.author_id, A.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, U.username "
                "FROM AUTHOR A "
                "INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE author_id = :id"
            )
            result = session.execute(sql, {"id": id})
            row = result.fetchone()
            if row:
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
                    'username': row[9]
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
            sql = text(
                "UPDATE AUTHOR SET student_code = :student_code WHERE author_id = :author_id; "
                "SET @person_id = (SELECT person_id FROM AUTHOR WHERE author_id = :author_id); "
                "UPDATE PERSON SET firstname = :firstname, lastname = :lastname, dni = :dni, phone = :phone, address = :address, email = :email "
                "WHERE person_id = @person_id; "
                "UPDATE USER SET username = :username "
                "WHERE person_id = @person_id; "
            )
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
            sql = text(
                "UPDATE PERSON AS p "
                "INNER JOIN AUTHOR AS a "
                "ON p.person_id = a.person_id "
                "SET p.is_deleted = 1 "
                "WHERE a.author_id = :id"
            )
            session.execute(sql, {"id": id})
            session.commit()
            return {'message': 'Autor created successfully'}, 200
        except Exception as ex:
            raise Exception(ex)