from models.Advisor import Advisor
from models.Person import Person
from sqlalchemy import text

class ControllerAdvisor():

    @classmethod
    def getAdvisors(cls, db):
        try:
            session = db.session()
            sql = text(
                "SELECT A.advisor_code, A.advisor_id, A.institution, A.person_id, P.firstname, P.lastname, P.phone, P.address, P.email "
                "FROM ADVISOR A INNER JOIN PERSON P "
                "ON A.person_id = P.person_id "
                "WHERE is_deleted = 0;"
            )
            result = session.execute(sql)
            rows=result.fetchall()
            advisors = []
            if rows != None:
                for row in rows:
                    advisor = Advisor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    advisors.append(advisor)
                return advisors
            else:
                return None
        except Exception as ex:
            raise Exception(ex)