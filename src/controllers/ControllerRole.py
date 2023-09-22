from models.Role import Role
from sqlalchemy import text

class ControllerRole():

    @classmethod
    def getRoles(cls, db):
        try:
            session = db.session()
            sql = text(
                "SELECT R.role_id, R.role "
                "FROM ROLE R "               
                "WHERE is_deleted = 0;"
            )
            result = session.execute(sql)
            rows=result.fetchall()
            roles = []
            if rows != None:
                for row in rows:
                    role = Role(row[0], row[1])
                    roles.append(role)
                return roles
            else:
                return None
        except Exception as ex:
            raise Exception(ex)