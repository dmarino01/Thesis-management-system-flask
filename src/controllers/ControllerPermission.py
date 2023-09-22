from models.Permission import Permission
from sqlalchemy import text

class ControllerPermission():

    @classmethod
    def getPermissions(cls, db):
        try:
            session = db.session()
            sql = text(
                "SELECT P.permission_id, P.permission, P.description "
                "FROM Permission P "               
                "WHERE is_deleted = 0;"
            )
            result = session.execute(sql)
            rows=result.fetchall()
            permissions = []
            if rows != None:
                for row in rows:
                    permission = Permission(row[0], row[1], row[2])
                    permissions.append(permission)
                return permissions
            else:
                return None
        except Exception as ex:
            raise Exception(ex)