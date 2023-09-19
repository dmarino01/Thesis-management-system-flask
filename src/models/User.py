from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, user_id, username, password, person_id) -> None:
        self.user_id = user_id
        self.username = username
        self.password = password
        self.person_id = person_id

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    def get_id(self):
        return str(self.user_id)

#print(generate_password_hash("Unitru@2023"))