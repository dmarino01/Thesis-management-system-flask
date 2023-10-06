from sqlalchemy import text

class ControllerAdmin():

    @classmethod
    def get_admin_by_person_id(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetAdminByPersonId(:person_id)")
            result = session.execute(sql, {"person_id": id})
            rows = result.fetchall()
            if rows:
                row = rows[0]
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