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
        
    #Search Role
    @classmethod
    def getRolesbyName(cls, db, name):
        try:
            session = db.session()
            sql = text(
                "SELECT R.role_id, R.role "
                "FROM ROLE "
                "WHERE is_deleted = 0 AND role LIKE :role"
            )
            result = session.execute(sql, {'name': f'%{name}%'})
            session.commit()
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
        
    #Create a New Role
    @classmethod    
    def createRole(cls, db, role):
        try:
            session = db.session()
            sql = text(
                "INSERT INTO ROLE (role) "
                "VALUES (:role); "
            )
            params = {
                'role': role               
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Role created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)
        
    #Get Role by ID
    @classmethod
    def get_role_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT R.role_id, R.role "
                "FROM ROLE R " 
                "WHERE role_id = :id"
            )
            result = session.execute(sql, {"id": id})
            session.commit()
            row = result.fetchone()
            if row:
                role = {
                    'role_id': row[0],
                    'role': row[1]
                }
                return role
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    #Update an Role info
    @classmethod
    def update_role(cls, db, id, role):
        try:
            session = db.session()
            sql = text(
                "UPDATE ROLE SET role = :role "
                "WHERE role_id = :role_id; "
            )
            params = {
                'role_id': id,
                'role': role               
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Role updated successfully'}, 200
        except Exception as ex:
            raise Exception(ex)
        
    #Logical deletion of a role
    @classmethod    
    def desactivate_role(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "UPDATE ROLE AS r "
                "SET r.is_deleted = 1 "
                "WHERE r.role_id = :role_id"
            )
            session.execute(sql, {"role_id": id})
            session.commit()
            return {'message': 'Role created successfully'}, 200
        except Exception as ex:
            raise Exception(ex)
        
    #Assign permissions to a role
    @classmethod
    def assign_permissions(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "INSERT INTO permission_role (permission_id, role_id) "
                "VALUES ('5', :role_id)"
            )
            session.execute(sql, {"role_id": id})
            session.commit()
            return {'message': 'Permissions assigned successfully'}, 200
        except Exception as ex:
            raise Exception(ex)