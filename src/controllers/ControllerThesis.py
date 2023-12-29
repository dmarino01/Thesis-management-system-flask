from flask_login import current_user
from models.Thesis import Thesis
from sqlalchemy import text

class ControllerThesis():

    #Method to get thesis by author_id
    @classmethod
    def getThesis(cls, db):
        try:
            user_id = current_user.user_id
            session = db.session()
            sql = text(
                "SELECT T.thesis_id, T.title, T.abstract, T.submission_date, T.expiration_date, T.last_update_date, R.rating, T.pdf_link, T.thesis_status_id, A.author_id, P.firstname, P.lastname "
                "FROM THESIS T "
                "INNER JOIN AUTHOR_THESIS AT ON AT.thesis_id = T.thesis_id "
                "INNER JOIN AUTHOR A ON A.author_id = AT.author_id "
                "INNER JOIN PERSON P ON P.person_id = A.person_id "
                "LEFT JOIN REVIEW R ON R.thesis_id = T.thesis_id "
                "INNER JOIN USER U ON U.person_id = P.person_id "
                "WHERE T.is_deleted = 0 AND U.user_id = :user_id"
            )
            result = session.execute(sql, {"user_id": user_id})
            session.commit()
            rows=result.fetchall()
            thesiss = []
            if rows != None:
                for row in rows:
                    thesis = Thesis(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                    thesiss.append(thesis)
                return thesiss
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    #Method to get thesis by thesis_id
    @classmethod
    def get_thesis_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT T.thesis_id, T.title, T.abstract, T.submission_date, R.rating, T.pdf_link, T.thesis_status_id, A.author_id, P.firstname, P.lastname "
                "FROM THESIS T " 
                "INNER JOIN AUTHOR_THESIS AT ON AT.thesis_id = T.thesis_id "
                "INNER JOIN AUTHOR A ON A.author_id = AT.author_id "
                "INNER JOIN PERSON P ON P.person_id = A.person_id "
                "LEFT JOIN REVIEW R ON R.thesis_id = T.thesis_id "
                "INNER JOIN USER U ON U.person_id = P.person_id "
                "WHERE T.thesis_id = :id"
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
                    'rating' : row[4],
                    'pdf_link' : row[5],
                    'thesis_status_id': row[6],
                    'author_id': row[7],
                    'firstname': row[8],
                    'lastname': row[9],
                }
                return thesis
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    #Method to save thesis
    @classmethod
    def createThesis(cls, db, title, abstract, pdf_link):
        try:
            person_id = current_user.person_id
            session = db.session()
            sql = text(
                "INSERT INTO THESIS (title, abstract, submission_date, pdf_link, thesis_status_id) "
                "VALUES (:title, :abstract, CURDATE(), :pdf_link, 1); "
                "SET @thesis_id = LAST_INSERT_ID(); "
                "SET @author_id = (SELECT author_id FROM author where person_id = :person_id); "
                "INSERT INTO AUTHOR_THESIS (author_id, thesis_id) "
                "VALUES (@author_id, @thesis_id);"
            )
            params = {
                'title': title,
                'abstract': abstract,
                'pdf_link': pdf_link,
                'person_id': person_id
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Thesis created successfully'}, 201
        except Exception as ex:
            raise Exception(ex)
    
    #Method to update thesis
    @classmethod
    def updateThesis(cls, db, id, title, abstract):
        try:
            session = db.session()
            sql = text(
                "UPDATE thesis "
                "SET title = :title, abstract = :abstract "
                "WHERE  thesis_id = :id; "
            )
            params = {
                'id': id,
                'title': title,
                'abstract': abstract
            }
            session.execute(sql, params)
            session.commit()
            return {'message': 'Thesis updated successfully'}, 200
        except Exception as ex:
            raise Exception(ex)
        
    #Logical deletion of an thesis
    @classmethod    
    def desactivate_thesis(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "UPDATE THESIS "
                "SET is_deleted = 1 "
                "WHERE thesis_id = :id"
            )
            session.execute(sql, {"id": id})
            session.commit()
            return {'message': 'Thesis created successfully'}, 200
        except Exception as ex:
            raise Exception(ex)