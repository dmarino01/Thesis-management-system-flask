from models.User import User

class ControllerUser():

    @classmethod
    def login(cls, db, user):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT id, username, email, password FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], row[2], User.check_password(row[3], user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor=db.connection.cursor()
            sql="SELECT id, username, email FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                return User(row[0], row[1], row[2], None) 
            else:
                return None
        except Exception as ex:
            raise Exception(ex)