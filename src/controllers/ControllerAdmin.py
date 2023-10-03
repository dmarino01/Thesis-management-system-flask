from models.Admin import Admin
from sqlalchemy import text
from werkzeug.security import generate_password_hash

class ControllerAdmin():

    @classmethod
    def get_admin_by_person_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT P.person_id, P.firstname, P.lastname, P.dni, P.phone, P.address, P.email, P.image, U.username "
                "FROM PERSON P "
                "INNER JOIN USER U "
                "ON U.person_id = P.person_id "
                "WHERE P.person_id = :id"
            )
            result = session.execute(sql, {"id": id})
            row = result.fetchone()
            if row:
                autor = {
                    'person_id': row[0],
                    'firstname': row[1],
                    'lastname': row[2],
                    'dni': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'email': row[6],
                    'image': row[7],
                    'username': row[8]
                }
                return autor
            else:
                return None
        except Exception as ex:
            raise Exception(ex)