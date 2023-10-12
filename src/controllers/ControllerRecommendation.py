from flask_login import current_user
from models.Recommendation import Recommendation
from models.Thesis import Thesis
from sqlalchemy import text

class ControllerRecommendation():

    @classmethod
    def get_thesis_by_author_advisor(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetThesisByAdvisor(:advisor_id);")
            params = {'advisor_id' : id}
            result = session.execute(sql, params)
            rows=result.fetchall()
            thesiss = []
            if rows != None:
                for row in rows:
                    thesis = Thesis(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
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
            sql = text(
                "SELECT R.recommendation_id, R.recommendation_date, R.recommendation_text, R.thesis_id, R.advisor_id, P.firstname, P.lastname, P.image "
                "FROM RECOMMENDATION R "
                "INNER JOIN ADVISOR A ON R.advisor_id = A.advisor_id "
                "INNER JOIN PERSON P ON P.person_id = A.person_id "
                "WHERE R.is_deleted = 0 AND R.thesis_id = :id;"
            )
            result = session.execute(sql, {"id": id})
            session.commit()
            rows = result.fetchall()
            recommendations = []
            if rows != None:
                for row in rows:
                    recommendation = Recommendation(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
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
                "SET @advisor_id = (select advisor_id from advisor where person_id = :person_id); "
                "INSERT INTO RECOMMENDATION (recommendation_date, recommendation_text, thesis_id, advisor_id) "
                "VALUES (:date, :recommendation_text, :thesis_id, @advisor_id)"
            )
            params = {
                'recommendation_text': recommendation_text,
                'date': date,
                'thesis_id': thesis_id,
                'person_id': person_id
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Autor created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def desactivate_recommendation(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "UPDATE RECOMMENDATION "
                "SET is_deleted = '1' "
                "WHERE recommendation_id = :id;"
            )
            params = {
                'id': id
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Recommendation deleted successfully'}, 200
        except Exception as ex:
            raise Exception(ex)