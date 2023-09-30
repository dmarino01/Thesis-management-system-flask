from flask_login import current_user
from models.Recommendation import Recommendation
from sqlalchemy import text

class ControllerRecommendation():

    @classmethod
    def get_recommendation_by_thesis_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT recommendation_id, recommendation_date, recommendation_text, thesis_id, advisor_id "
                "FROM RECOMMENDATION "
                "WHERE thesis_id = :id"
            )
            result = session.execute(sql, {"id": id})
            session.commit()
            row = result.fetchone()
            if row:
                recommendation = {
                    'recommendation_id': row[0],
                    'recommendation_date': row[1],
                    'recommendation_text' : row[2],
                    'thesis_id' : row[3],
                    'advisor_id': row[4]
                }
                return recommendation
            else:
                return None
        except Exception as ex:
            raise Exception(ex)