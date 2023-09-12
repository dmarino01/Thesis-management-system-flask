from models.Autor import Autor

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