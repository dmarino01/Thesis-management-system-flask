from flask_login import current_user
from models.Review import Review
from models.Thesis import Thesis
from sqlalchemy import text


class ControllerReview:
    @classmethod
    def get_thesis_by_review_reviewer(
        cls, db, id, project_filter=None, status_filter=None
    ):
        try:
            session = db.session()
            # sql = text("CALL GetThesisByReviewer(:person_id);")
            sql = text(
                "SELECT DISTINCT T.thesis_id, T.title, T.abstract, T.submission_date, T.expiration_date, T.last_update_date, T.rating, T.pdf_link, T.turnitin_link, T.article_link, T.thesis_status_id, T.project_id, Aut.author_id, P.firstname, P.lastname "
                "FROM thesis T "
                "INNER JOIN AUTHOR_THESIS AT ON T.thesis_id = AT.thesis_id "
                "INNER JOIN AUTHOR Aut ON Aut.author_id = AT.author_id "
                "INNER JOIN PERSON P ON P.person_id = Aut.person_id "
                "LEFT JOIN REVIEW R ON R.thesis_id = T.thesis_id "
                "INNER JOIN REVIEWER_THESIS R_T ON T.thesis_id = R_T.thesis_id "
                "INNER JOIN REVIEWER Rev ON Rev.reviewer_id = R_T.reviewer_id "
                "INNER JOIN PERSON PA ON PA.person_id = Rev.person_id "
                "WHERE T.is_deleted = 0 AND P.is_deleted = 0 AND PA.person_id = :p_person_id"
            )

            # Add filters based on project_id
            if project_filter is not None:
                sql += " AND T.project_id = :project_id"

            # Add filters based on thesis_status_id
            if status_filter is not None:
                sql += " AND T.thesis_status_id = :status_id"

            result = session.execute(
                sql,
                {
                    "p_person_id": id,
                    "project_id": project_filter,
                    "status_id": status_filter,
                },
            )
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
                    )
                    thesiss.append(thesis)
                return thesiss
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def createReview(cls, db, nota, comentario, id, person_id, date):
        try:
            session = db.session()
            sql = text(
                "CALL CreateReview(:nota, :comment, :thesis_id, :person_id, :date)"
            )
            params = {
                "nota": nota,
                "comment": comentario,
                "thesis_id": id,
                "person_id": person_id,
                "date": date,
            }
            session.execute(sql, params)
            session.commit()
            return {"message": "Review created successfully"}, 201
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def check_review_exists(cls, db, id, person_id):
        try:
            session = db.session()

            # First, retrieve the reviewer_id
            reviewer_id_query = text(
                "SELECT reviewer_id FROM REVIEWER WHERE person_id = :p_person_id"
            )
            reviewer_id_result = session.execute(
                reviewer_id_query, {"p_person_id": person_id}
            )
            reviewer_id = reviewer_id_result.scalar()

            # Check if a review exists for the given thesis and reviewer_id
            review_query = text(
                "SELECT * FROM REVIEW WHERE thesis_id = :p_thesis_id AND reviewer_id = :p_reviewer_id"
            )
            review_result = session.execute(
                review_query, {"p_thesis_id": id, "p_reviewer_id": reviewer_id}
            )
            review_exists = review_result.fetchone() is not None

            return review_exists
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_review_details_by_thesis_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "select p.firstname, p.lastname, p.image, r.rating, r.review_date, r.comment "
                "from review r "
                "inner join reviewer rw on rw.reviewer_id = r.reviewer_id "
                "inner join person p on rw.person_id = p.person_id "
                "where thesis_id = :p_thesis_id; "
            )
            params = {
                "p_thesis_id": id,
            }
            result = session.execute(sql, params)
            session.close()
            return result
        except Exception as ex:
            raise Exception(ex)
