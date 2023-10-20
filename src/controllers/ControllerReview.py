from flask_login import current_user
from models.Review import Review
from models.Thesis import Thesis
from sqlalchemy import text

class ControllerReview():

    @classmethod
    def get_thesis_by_author_reviewer(cls, db, id):
        try:
            session = db.session()
            sql = text("CALL GetThesisByReviewer(:person_id);")
            params = {'person_id' : id}
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
    def createReview(cls, db, nota, comentario, id, person_id, date):
        try:
            session = db.session()
            sql = text(
            "SET @reviewer_id = (select reviewer_id from reviewer where person_id = :person_id); "    
            "INSERT INTO REVIEW (thesis_id, review_date, rating, reviewer_id, comment) "
            "VALUES (:thesis_id, :date, :nota, @reviewer_id, :comment); "
            "UPDATE thesis SET thesis_status_id = '2' WHERE thesis_id = :thesis_id; "
            )
            params = {
                'nota' : nota,
                'comment' : comentario,
                'thesis_id' : id,
                'person_id' : person_id,
                'date' : date
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Review created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)