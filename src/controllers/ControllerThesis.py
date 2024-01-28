from flask_login import current_user
from models.Thesis import Thesis
from models.Unit import Unit
from models.Mention import Mention
from sqlalchemy import text


class ControllerThesis:
    # Method to get thesis by author_id
    @classmethod
    def getThesis(cls, db, project_filter=None, status_filter=None):
        try:
            user_id = current_user.user_id
            session = db.session()
            
            sql = text(
                "SELECT DISTINCT T.thesis_id, T.title, T.abstract, T.submission_date, T.expiration_date, T.last_update_date, T.rating, T.pdf_link, T.turnitin_porcentaje, T.turnitin_link, T.article_link, T.thesis_status_id, T.project_id, T.mention_id, M.name, A.author_id, P.firstname, P.lastname "
                "FROM THESIS T "
                "INNER JOIN MENTION M ON M.id = T.mention_id "
                "INNER JOIN AUTHOR_THESIS AT ON AT.thesis_id = T.thesis_id "
                "INNER JOIN AUTHOR A ON A.author_id = AT.author_id "
                "INNER JOIN PERSON P ON P.person_id = A.person_id "
                "LEFT JOIN REVIEW R ON R.thesis_id = T.thesis_id "
                "INNER JOIN USER U ON U.person_id = P.person_id "
                "WHERE T.is_deleted = 0 AND U.user_id = :user_id"
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
                    "user_id": user_id,
                    "project_id": project_filter,
                    "status_id": status_filter,
                },
            )
            session.commit()
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

    # Method to get thesis by thesis_id
    @classmethod
    def get_thesis_by_id(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "SELECT T.thesis_id, T.title, T.abstract, T.submission_date, T.expiration_date, T.last_update_date, T.rating, T.pdf_link, T.turnitin_porcentaje, T.turnitin_link, T.article_link, T.thesis_status_id, T.project_id, T.mention_id, M.name, A.author_id, P.firstname, P.lastname "
                "FROM THESIS T "
                "INNER JOIN MENTION M ON M.id = T.mention_id "
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
                    "thesis_id": row[0],
                    "title": row[1],
                    "abstract": row[2],
                    "submission_date": row[3],
                    "expiration_date": row[4],
                    "last_update_date": row[5],
                    "rating": row[6],
                    "pdf_link": row[7],
                    "turnitin_porcentaje": row[8],
                    "turnitin_link": row[9],
                    "article_link": row[10],
                    "thesis_status_id": row[11],
                    "project_id": row[12],
                    "mention_id": row[13],
                    "mention": row[14],
                    "author_id": row[15],
                    "firstname": row[16],
                    "lastname": row[17],
                }
                return thesis
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    # Method to save thesis project
    @classmethod
    def createProjectThesis(
        cls,
        db,
        title,
        abstract,
        project_id,
        pdf_link,
        turnitin_link,
        turnitin_porcentaje,
        expiration_date,
        mencion,
        project_creation_date,
    ):
        try:
            person_id = current_user.person_id
            session = db.session()
            sql = text(
                "INSERT INTO THESIS (title, abstract, submission_date, uploaded_to_sys_date, expiration_date, last_update_date, pdf_link, turnitin_link, turnitin_porcentaje, thesis_status_id, project_id, mention_id) "
                "VALUES ( "
                "    :title, :abstract, :project_creation_date, CURDATE(), "
                "    CASE "
                "        WHEN :expiration_date IS NOT NULL AND :expiration_date != '' THEN :expiration_date "
                "        ELSE DATE_ADD(CURDATE(), INTERVAL 2 YEAR) "
                "    END, "
                "    CURDATE(), "
                "    :pdf_link, :turnitin_link, :turnitin_porcentaje, 1, :project_id, :mention_id "
                "    ); "
                "SET @thesis_id = LAST_INSERT_ID(); "
                "SET @author_id = (SELECT author_id FROM author where person_id = :person_id); "
                "INSERT INTO AUTHOR_THESIS (author_id, thesis_id) "
                "VALUES (@author_id, @thesis_id);"
            )
            params = {
                "title": title,
                "abstract": abstract,
                "project_id": project_id,
                "pdf_link": pdf_link,
                "turnitin_link": turnitin_link,
                "turnitin_porcentaje": turnitin_porcentaje,
                "expiration_date": expiration_date,
                "person_id": person_id,
                "mention_id": mencion,
                "project_creation_date": project_creation_date,
            }
            session.execute(sql, params)
            session.commit()
            return {"message": "Thesis project created successfully"}, 201
        except Exception as ex:
            raise Exception(ex)

    # Method to save dissertion thesis
    @classmethod
    def createDissertationThesis(
        cls,
        db,
        title,
        abstract,
        project_id,
        pdf_link,
        pdf_turnitin_link,
        pdf_article_link,
        expiration_date,
        mencion,
        project_creation_date,
    ):
        try:
            person_id = current_user.person_id
            session = db.session()

            sql = text(
                "INSERT INTO THESIS (title, abstract, submission_date, uploaded_to_sys_date, expiration_date, last_update_date, pdf_link, turnitin_link, article_link, thesis_status_id, project_id, mention_id) "
                "VALUES ( "
                "    :title, :abstract, :project_creation_date, CURDATE(), "
                "    CASE "
                "        WHEN :expiration_date IS NOT NULL AND :expiration_date != '' THEN :expiration_date "
                "        ELSE DATE_ADD(CURDATE(), INTERVAL 2 YEAR) "
                "    END, "
                "    CURDATE(), "
                "    :pdf_link, :turnitin_link, :article_link, 1, :project_id, :mention_id "
                "    ); "
                "SET @thesis_id = LAST_INSERT_ID(); "
                "SET @author_id = (SELECT author_id FROM author where person_id = :person_id); "
                "INSERT INTO AUTHOR_THESIS (author_id, thesis_id) "
                "VALUES (@author_id, @thesis_id);"
            )
            params = {
                "title": title,
                "abstract": abstract,
                "project_id": project_id,
                "pdf_link": pdf_link,
                "turnitin_link": pdf_turnitin_link,
                "article_link": pdf_article_link,
                "expiration_date": expiration_date,
                "person_id": person_id,
                "mention_id": mencion,
                "project_creation_date": project_creation_date,
            }
            session.execute(sql, params)
            session.commit()
            return {"message": "Thesis project created successfully"}, 201
        except Exception as ex:
            raise Exception(ex)

    # Method to update thesis
    @classmethod
    def updateThesis(cls, db, id, title, abstract, new_filename, new_filename_turnitin, turnitin_porcentaje):
        try:
            session = db.session()
            sql = text(
                "UPDATE thesis "
                "SET title = :title, abstract = :abstract, pdf_link = :new_filename, turnitin_link = :new_filename_turnitin, turnitin_porcentaje = :turnitin_porcentaje "
                "WHERE  thesis_id = :id; "
            )
            params = {
                "id": id,
                "title": title,
                "abstract": abstract,
                "new_filename": new_filename,
                "new_filename_turnitin": new_filename_turnitin,
                "turnitin_porcentaje": turnitin_porcentaje,
            }
            session.execute(sql, params)
            session.commit()
            return {"message": "Thesis updated successfully"}, 200
        except Exception as ex:
            raise Exception(ex)

    # Logical deletion of an thesis
    @classmethod
    def desactivate_thesis(cls, db, id):
        try:
            session = db.session()
            sql = text("UPDATE THESIS " "SET is_deleted = 1 " "WHERE thesis_id = :id")
            session.execute(sql, {"id": id})
            session.commit()
            return {"message": "Thesis created successfully"}, 200
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def check_dissertation_exists(cls, db, id):
        try:
            session = db.session()
            sql = text("select * from thesis where project_id = :id and is_deleted = 0")
            params = {
                "id": id,
            }
            dissertation_result = session.execute(sql, params)
            dissertation_exists = dissertation_result.fetchone() is not None
            return dissertation_exists
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getThesisWithoutReviewers(cls, db):
        try:
            session = db.session()
            sql = text("SELECT * FROM thesis_without_reviewer_assigned_info;")
            result = session.execute(sql)
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getTotalThesis(cls, db):
        try:
            session = db.session()
            sql = text("SELECT COUNT(*) FROM thesis;")
            result = session.execute(sql)
            count = result.fetchone()[0]
            return count
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getTotalThesisWithoutReviewer(cls, db):
        try:
            session = db.session()
            sql = text("SELECT COUNT(*) FROM thesis_without_reviewer_assigned_info;")
            result = session.execute(sql)
            count = result.fetchone()[0]
            return count
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getThesisWithoutReviews(cls, db):
        try:
            session = db.session()
            sql = text("SELECT * FROM thesis_without_reviews_assigned_info;")
            result = session.execute(sql)
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getTotalThesisWithoutReviews(cls, db):
        try:
            session = db.session()
            sql = text("SELECT COUNT(*) FROM thesis_without_reviews_assigned_info;")
            result = session.execute(sql)
            count = result.fetchone()[0]
            return count
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def createSignThesis(cls, db, image, id):
        try:
            session = db.session()
            sql = text(
                "INSERT INTO sign_review_thesis(link, thesis_id) VALUES (:image, :id);"
            )
            params = {"image": image, "id": id}
            session.execute(sql, params)
            session.commit()
            return {"message": "Sign Review Thesis created successfully"}, 201
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_link_sign(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "select srt.link from thesis t "
                "left join sign_review_thesis srt on srt.thesis_id = t.thesis_id "
                "where srt.link is not null and t.thesis_id = :p_thesis_id;"
            )
            params = {"p_thesis_id": id}
            result = session.execute(sql, params)
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_sign_if_exists(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "select srt.link from thesis t "
                "left join sign_review_thesis srt on srt.thesis_id = t.thesis_id "
                "where srt.link is not null and t.thesis_id = :p_thesis_id;"
            )
            params = {"p_thesis_id": id}
            result = session.execute(sql, params)
            sign_exists = result.fetchone() is not None
            return sign_exists
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getThesisForAdmin(cls, db, project_filter=None, status_filter=None):
        try:
            session = db.session()
            
            sql = text(
                "SELECT DISTINCT T.thesis_id, T.title, T.abstract, T.submission_date, T.expiration_date, T.last_update_date, T.rating, T.pdf_link, T.turnitin_porcentaje, T.turnitin_link, T.article_link, T.thesis_status_id, T.project_id, T.mention_id, M.name, A.author_id, P.firstname, P.lastname "
                "FROM THESIS T "
                "INNER JOIN MENTION M ON M.id = T.mention_id "
                "INNER JOIN AUTHOR_THESIS AT ON AT.thesis_id = T.thesis_id "
                "INNER JOIN AUTHOR A ON A.author_id = AT.author_id "
                "INNER JOIN PERSON P ON P.person_id = A.person_id "
                "LEFT JOIN REVIEW R ON R.thesis_id = T.thesis_id "
                "INNER JOIN USER U ON U.person_id = P.person_id "
                "WHERE T.is_deleted = 0"
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
                    "project_id": project_filter,
                    "status_id": status_filter,
                },
            )
            session.commit()
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
    def getAllUnits(cls, db):
        try:
            session = db.session()
            sql = text("SELECT * FROM unit")
            result = session.execute(sql, {"id": id})
            rows = result.fetchall()
            units = []
            if rows != None:
                for row in rows:
                    unit = Unit(
                        row[0],
                        row[1],
                        row[2]
                    )
                    units.append(unit)
                return units
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getAllMentionsById(cls, db, id):
        try:
            session = db.session()
            sql = text("SELECT * FROM mention WHERE unit_id = :unit_id;")
            result = session.execute(sql, {"unit_id": id})
            rows = result.fetchall()
            mentions = []
            if rows != None:
                for row in rows:
                    mention = Mention(
                        row[0],
                        row[1],
                        row[2],
                        row[3]
                    )
                    mentions.append(mention)
                return mentions
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getUnitByMention(cls, db, id):
        try:
            session = db.session()
            sql = text(
                "select U.name from thesis t "
                "inner join mention m on m.id = t.mention_id "
                "inner join unit u on u.id = m.unit_id "
                "where t.thesis_id = :id"
                )
            result = session.execute(sql, {"id": id})
            unit = result.scalar()
            result.close()
            return unit
        except Exception as ex:
            raise Exception(ex)

