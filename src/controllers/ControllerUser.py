from models.User import User
from sqlalchemy import text

class ControllerUser():

    @classmethod
    def login(cls, db, user):
        try:
            session = db.session()
            sql = text(
                "SELECT u.user_id, u.username, u.password, u.person_id FROM user u "
                "INNER JOIN person p on p.person_id = u.person_id "
                "WHERE p.is_deleted = 0 AND u.username = :username"
            )
            result = session.execute(sql, {"username": user.username})
            row = result.fetchone()
            if row is not None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

        
    @classmethod
    def get_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text("SELECT user_id, username FROM user WHERE user_id = :user_id")
            result = session.execute(sql, {"user_id": id})
            row = result.fetchone()
            if row is not None:
                return User(row[0], row[1], None, None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
