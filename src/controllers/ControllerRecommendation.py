from flask_login import current_user
from models.Recommendation import Recommendation
from models.Thesis import Thesis
from sqlalchemy import text


class ControllerRecommendation:
    @classmethod
    def get_thesis_by_author_advisor(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetThesisByAdvisor(:p_person_id);")
            result = session.execute(sql, {"p_person_id": id})
            rows = result.fetchall()
            thesiss = []
            if rows != None:
                for row in rows:
                    thesis = Thesis(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9],
                        row[10],
                        row[11],
                        row[12],
                        row[13],
                        row[14],
                        row[15],
                        row[16],
                        row[17]
                    )
                    thesiss.append(thesis)
                return thesiss
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_recommendations_by_thesis_id(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetRecommendationsById(:id)")
            result = session.execute(sql, {"id": id})
            rows = result.fetchall()
            recommendations = []
            if rows != None:
                for row in rows:
                    recommendation = Recommendation(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                    )
                    recommendations.append(recommendation)
                return recommendations
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def createRecommendation(cls, db, recommendation_text, date, thesis_id, person_id):
        try:
            session = db.session()
            sql = text(
                "CALL CreateRecommendation(:date, :recommendation_text, :thesis_id, :person_id)"
            )
            params = {
                "recommendation_text": recommendation_text,
                "date": date,
                "thesis_id": thesis_id,
                "person_id": person_id,
            }
            session.execute(sql, params)
            session.commit()
            return {"message": "Autor created successfully"}, 201
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def desactivate_recommendation(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL DesactivateRecommendation(:id)")
            params = {"id": id}
            session.execute(sql, params)
            session.commit()
            return {"message": "Recommendation deleted successfully"}, 200
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def authorize_review(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL AuthorizeReview(:id)")
            params = {"id": id}
            session.execute(sql, params)
            session.commit()
            return {"message": "Authorization of thesis was successful"}, 200
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def clear_recommendation(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL ClearRecommendation(:p_recommendation_id)")
            params = {
                "p_recommendation_id": id,
            }
            session.execute(sql, params)
            session.commit()
            return {"message": "Authorization of thesis was successful"}, 200
        except Exception as ex:
            raise Exception(ex)
