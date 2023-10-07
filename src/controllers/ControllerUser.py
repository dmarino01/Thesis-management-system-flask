import base64
from models.User import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash

class ControllerUser():

    @classmethod
    def login(cls, db, user):
        try:
            session = db.session()
            sql = text("CALL Login(:username);")
            result = session.execute(sql, {"username": user.username})
            rows = result.fetchall()
            if rows:
                row = rows[0]
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], None, None)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

        
    @classmethod
    def get_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetUserById(:user_id);")
            params = {"user_id": id}
            result = session.execute(sql, params)
            rows = result.fetchall()
            session.close()

            if rows:
                row = rows[0]
                return User(row[0], row[1], row[2], row[3], row[4], row[5])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


        
    #Update User
    @classmethod
    def update_user(cls, db, id, student_code, reviewer_code, advisor_code, institution, grade, firstname, lastname, dni, phone, address, email, image, username, password):
        try:
            session = db.session()
            hashed_password = ''
            if password != '':
                hashed_password = generate_password_hash(password)  
            sql = text("CALL UpdateUser(:person_id, :firstname, :lastname, :dni, :phone, :address, :email, :image, :username, :password, :student_code, :advisor_code, :institution, :reviewer_code, :grade)")
            params = {
                'person_id': id,
                'firstname': firstname,
                'lastname': lastname,
                'dni': dni,
                'phone': phone,
                'address': address,
                'email': email,
                'image': image,
                'username': username,
                'password': hashed_password,
                'student_code': student_code,
                'advisor_code': advisor_code,
                'institution': institution,
                'reviewer_code': reviewer_code,
                'grade': grade,
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'User updated successfully'}, 200
        except Exception as ex:
            raise Exception(ex)


    #Update User
    @classmethod
    def remove_image_user(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL RemoveImageUser(:person_id);")
            params = {'person_id': id}
            session.execute(sql, params)
            session.commit()
            return {'message': 'Image removed successfully'}, 200
        except Exception as ex:
            raise Exception(ex)
