from flask_login import current_user
from models.Thesis import Thesis
from sqlalchemy import text

class ControllerThesis():

    @classmethod
    def getThesis(cls, db):
        try:
            user_id = current_user.user_id
            session = db.session()
            sql = text(
                "SELECT T.thesis_id, T.title, T.abstract, T.submission_date, T.thesis_status_id "
                "FROM THESIS T "
                "INNER JOIN AUTHOR_THESIS AT ON AT.thesis_id = T.thesis_id "
                "INNER JOIN AUTHOR A ON A.author_id = AT.author_id "
                "INNER JOIN PERSON P ON P.person_id = A.person_id "
                "INNER JOIN USER U ON U.person_id = P.person_id "
                "WHERE T.is_deleted = 0 AND U.user_id = :user_id"
            )
            result = session.execute(sql, {"user_id": user_id})
            session.commit()
            rows=result.fetchall()
            thesiss = []
            if rows != None:
                for row in rows:
                    thesis = Thesis(row[0], row[1], row[2], row[3], row[4])
                    thesiss.append(thesis)
                return thesiss
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_thesis_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT T.thesis_id, T.title, T.abstract, T.submission_date, thesis_status_id "
                "FROM THESIS T " 
                "WHERE thesis_id = :id"
            )
            result = session.execute(sql, {"id": id})
            session.commit()
            row = result.fetchone()
            if row:
                thesis = {
                    'thesis_id': row[0],
                    'title': row[1],
                    'abstract' : row[2],
                    'submission_date' : row[3],
                    'thesis_status_id': row[4]
                }
                return thesis
            else:
                return None
        except Exception as ex:
            raise Exception(ex)