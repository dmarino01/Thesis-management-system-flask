from models.Autor import Autor
from flask_mysqldb import MySQL

mysql = MySQL()

class ControllerAutor():

    @classmethod
    def getAutors(cls, db):
        try:
            cursor=db.connection.cursor()
            sql="SELECT * FROM autor WHERE is_deleted = 0"
            cursor.execute(sql)
            rows=cursor.fetchall()
            autores = []
            if rows != None:
                for row in rows:
                    autor = Autor(row[0], row[1], row[2], row[3], row[4])
                    autores.append(autor)
                return autores
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod    
    def createAutor(cls, db, firstname, lastname, email, phone):
        try:
            cursor = db.connection.cursor()
            # Assuming you have a MySQL table named 'autors'
            cursor.execute("INSERT INTO autor (firstname, lastname, email, phone) VALUES (%s, %s, %s, %s)",
                        (firstname, lastname, email, phone))
            db.connection.commit()
            cursor.close()
            return {'message': 'Autor created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_autor_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM autor WHERE id = %s", (id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                autor = {
                    'id': row[0],
                    'firstname': row[1],
                    'lastname': row[2],
                    'email': row[3],
                    'phone': row[4],
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