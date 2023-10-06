from flask_login import current_user
from models.Review import Review
from sqlalchemy import text

class ControllerReview():

    @classmethod
    def save_review(cls, db):
        try:
            return {'message': 'Review created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)