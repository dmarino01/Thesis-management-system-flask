class Recommendation():

    def __init__(self, recommendation_id, recommendation_date, recommendation_text, thesis_id, advisor_id, is_deleted=False):
        self.recommendation_id = recommendation_id
        self.recommendation_date = recommendation_date
        self.recommendation_text = recommendation_text
        self.thesis_id = thesis_id
        self.advisor_id = advisor_id
        self.is_deleted = is_deleted

    def __init__(self, recommendation_id, recommendation_date, recommendation_text, thesis_id, advisor_id, firstname, lastname, image, status, is_deleted=False):
        self.recommendation_id = recommendation_id
        self.recommendation_date = recommendation_date
        self.recommendation_text = recommendation_text
        self.thesis_id = thesis_id
        self.advisor_id = advisor_id
        self.firstname = firstname
        self.lastname = lastname
        self.image = image
        self.status = status
        self.is_deleted = is_deleted