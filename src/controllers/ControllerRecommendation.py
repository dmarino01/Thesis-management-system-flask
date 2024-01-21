from flask_login import current_user
from models.Recommendation import Recommendation
from models.Thesis import Thesis
from sqlalchemy import text


class ControllerRecommendation:
    @classmethod
    def get_thesis_by_author_advisor(cls, db, id, project_filter=None, status_filter=None):
        try:
            session = db.session()
            #sql = text("CALL GetThesisByAdvisor(:person_id);")
            sql = text(
                    "SELECT DISTINCT T.thesis_id, T.title, T.abstract, T.submission_date, T.expiration_date, T.last_update_date, "
                    "T.rating, T.pdf_link, T.turnitin_porcentaje, T.turnitin_link, T.article_link, T.thesis_status_id, T.project_id, Aut.author_id, P.firstname, P.lastname "
                    "FROM THESIS T "
                    "INNER JOIN AUTHOR_THESIS AT ON T.thesis_id = AT.thesis_id "
                    "LEFT JOIN REVIEW R ON R.thesis_id = T.thesis_id "
                    "INNER JOIN AUTHOR Aut ON Aut.author_id = AT.author_id "
                    "INNER JOIN PERSON P ON P.person_id = Aut.person_id "
                    "INNER JOIN ADVISOR_THESIS A_T ON t.thesis_id = A_T.thesis_id "
                    "INNER JOIN ADVISOR Adv ON Adv.advisor_id = A_T.advisor_id "
                    "INNER JOIN PERSON PA ON PA.person_id = Adv.person_id "
                    "WHERE T.is_deleted = 0 AND P.is_deleted = 0 AND PA.person_id = :p_person_id"
            )
            # Add filters based on project_id
            if project_filter is not None:
                sql += " AND T.project_id = :project_id"

            # Add filters based on thesis_status_id
            if status_filter is not None:
                sql += " AND T.thesis_status_id = :status_id"

            params = {
                "p_person_id": id,
                "project_id": project_filter,
                "status_id": status_filter,
            }
            result = session.execute(sql, params)
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
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
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