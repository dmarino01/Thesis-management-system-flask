from models.User import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash

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
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], None)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

        
    @classmethod
    def get_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT U.user_id, U.username, U.password, U.person_id, R.role "
                "FROM USER U "
                "INNER JOIN ROLE_USER RU "
                "ON RU.user_id = U.user_id "
                "INNER JOIN ROLE R "
                "ON RU.role_id = R.role_id "
                "WHERE U.user_id = :user_id"
            )
            result = session.execute(sql, {"user_id": id})
            row = result.fetchone()
            if row is not None:
                return User(row[0], row[1], row[2], row[3], row[4])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_user(cls, db, id, student_code, reviewer_code, advisor_code, grade, firstname, lastname, dni, phone, address, email, username, password):
        try:
            session = db.session()
            hashed_password = generate_password_hash(password)

            if student_code != '':
                sql = text(
                    "UPDATE PERSON "
                    "SET firstname = :firstname, lastname = :lastname, dni = :dni, phone = :phone, address = :address, email = :email "
                    "WHERE person_id = :person_id; "
                    "UPDATE USER "
                    "SET username = :username, "
                    "password = CASE WHEN :password <> '' THEN :password ELSE password END "
                    "WHERE person_id = :person_id; "
                    "UPDATE AUTHOR SET student_code = :student_code "
                    "WHERE person_id = :person_id;"
                )
            elif advisor_code != '':
                sql = text(
                    "UPDATE PERSON "
                    "SET firstname = :firstname, lastname = :lastname, dni = :dni, phone = :phone, address = :address, email = :email "
                    "WHERE person_id = :person_id; "
                    "UPDATE USER "
                    "SET username = :username, "
                    "password = CASE WHEN :password <> '' THEN :password ELSE password END "
                    "WHERE person_id = :person_id; "
                    "UPDATE ADVISOR SET advisor_code = :advisor_code "
                    "WHERE person_id = :person_id;"
                )
            elif reviewer_code != '':
                sql = text(
                    "UPDATE PERSON "
                    "SET firstname = :firstname, lastname = :lastname, dni = :dni, phone = :phone, address = :address, email = :email "
                    "WHERE person_id = :person_id; "
                    "UPDATE USER "
                    "SET username = :username, "
                    "password = CASE WHEN :password <> '' THEN :password ELSE password END "
                    "WHERE person_id = :person_id; "
                    "UPDATE reviewer SET reviewer_code = :reviewer_code, grade = :grade "
                    "WHERE person_id = :person_id;"
                )

            params = {
                'student_code': student_code,
                'reviewer_code': reviewer_code,
                'advisor_code': advisor_code,
                'grade': grade,
                'person_id': id,
                'firstname': firstname,
                'lastname': lastname,
                'dni': dni,
                'phone': phone,
                'address': address,
                'email': email,
                'username': username,
                'password': hashed_password
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'User updated successfully'}, 200
        except Exception as ex:
            raise Exception(ex)

