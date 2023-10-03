import base64
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, user_id, username, password, person_id) -> None:
        self.user_id = user_id
        self.username = username
        self.password = password
        self.person_id = person_id

    def __init__(self, user_id, username, password, person_id, role, image) -> None:
        self.user_id = user_id
        self.username = username
        self.password = password
        self.person_id = person_id
        self.role = role
        self.image = image

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    def get_id(self):
        return str(self.user_id)
    
    def decode_image(self):
        try:
            if self.image:
                return base64.b64decode(self.image)
        except Exception as ex:
            raise Exception(ex)
        return None