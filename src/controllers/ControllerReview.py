from models.Thesis import Thesis
from sqlalchemy import text


class ControllerReview:
    @classmethod
    def get_thesis_by_review_reviewer(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetThesisByReviewer(:p_person_id);")
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
                "SELECT DISTINCT rw.reviewer_id, p.firstname, p.lastname, p.image, r.rating, r.review_date, r.comment, r_r.role "
                "FROM "
                "    review r "
                "INNER JOIN thesis t ON t.thesis_id = r.thesis_id "
                "INNER JOIN reviewer rw ON rw.reviewer_id = r.reviewer_id "
                "INNER JOIN person p ON p.person_id = rw.person_id "
                "LEFT JOIN reviewer_thesis r_t ON r_t.reviewer_id = r.reviewer_id AND r_t.thesis_id = r.thesis_id "
                "INNER JOIN reviewer_role r_r ON r_r.id = r_t.reviewer_role_id "
                "where r.thesis_id = :p_thesis_id"
            )
            params = {
                "p_thesis_id": id,
            }
            result = session.execute(sql, params)
            session.close()
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getStatusReview(cls, db, id):
        try:
            session = db.session()

            sql = text("CALL getStatusReviewThesis(:p_thesis_id)")
            params = {
                "p_thesis_id": id,
            }
            result = session.execute(sql, params)
            status_review = result.scalar()
            result.close()
            return status_review
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getLastReviewDate(cls, db, id):
        try:
            session = db.session()

            sql = text(
                "SELECT p.firstname, p.lastname, p.image, r.rating, MAX(r.review_date) as review_date, r.comment, r_r.role "
                "FROM review r "
                "INNER JOIN thesis t ON t.thesis_id = r.thesis_id "
                "INNER JOIN reviewer_thesis r_t ON r_t.thesis_id = t.thesis_id "
                "INNER JOIN reviewer_role r_r ON r_r.id = r_t.reviewer_role_id "
                "INNER JOIN reviewer rw ON rw.reviewer_id = r_t.reviewer_id "
                "INNER JOIN person p ON p.person_id = rw.person_id "
                "WHERE r_t.thesis_id = :p_thesis_id "
                "ORDER BY r.review_date DESC "
                "LIMIT 1; "
            )
            params = {
                "p_thesis_id": id,
            }
            result = session.execute(sql, params)
            last_date = result.fetchone()
            result.close()
            return last_date
        except Exception as ex:
            raise Exception(ex)
