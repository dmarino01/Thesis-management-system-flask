from models.Author import Author
from models.Person import Person
from sqlalchemy import text

class ControllerAuthor():

    @classmethod
    def getAutors(cls, db):
        try:
            session = db.session()
            sql = text("SELECT A.student_code, A.author_id, A.person_id, P.firstname, P.lastname, P.phone, P.address, P.email FROM AUTHOR A INNER JOIN PERSON P ON A.person_id = P.person_id WHERE is_deleted = 0;")
            result = session.execute(sql)
            rows=result.fetchall()
            autores = []
            if rows != None:
                for row in rows:
                    autor = Author(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    autores.append(autor)
                return autores
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod    
    def createAutor(cls, db, firstname, lastname, email, phone):
        try:
            session = db.session()
            sql = text("INSERT INTO autor (firstname, lastname, email, phone) VALUES (%s, %s, %s, %s)",
                        (firstname, lastname, email, phone))
            session.execute(sql)
            session.commit()
            return {'message': 'Autor created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_autor_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text("SELECT A.student_code, A.author_id, A.person_id, P.firstname, P.lastname, P.phone, P.address, P.email FROM AUTHOR A INNER JOIN PERSON P ON A.person_id = P.person_id WHERE author_id = :id")
            result = session.execute(sql, {"id": id})
            row = result.fetchone()
            if row:
                autor = {
                    'student_code': row[0],
                    'author_id': row[1],
                    'person_id': row[2],
                    'firstname': row[3],
                    'lastname': row[4],
                    'phone': row[5],
                    'address': row[6],
                    'email': row[7]
                }
                return autor
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_autor(cls, db, id, firstname, lastname, email, phone):
        try:
            cursor = db.connection.cursor()
            cursor.execute("UPDATE autor SET firstname = %s, lastname = %s, email = %s, phone = %s WHERE id = %s",
                        (firstname, lastname, email, phone, id))
            db.connection.commit()
            cursor.close()
            return {'message': 'Autor updated successfully'}, 200

        except Exception as ex:
            raise Exception(ex)