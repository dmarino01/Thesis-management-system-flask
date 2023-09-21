class Reviewer():

    def __init__(self, reviewer_code, grade, person_id, reviewer_id):
        self.reviewer_code = reviewer_code
        self.grade = grade
        self.person_id = person_id
        self.reviewer_id = reviewer_id

    def __init__(self, reviewer_code, reviewer_id, grade, person_id, firstname, lastname, phone, address, email, is_deleted=False):
        self.reviewer_code = reviewer_code
        self.reviewer_id = reviewer_id
        self.grade = grade
        self.person_id = person_id    
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.address = address
        self.email = email
        self.is_deleted = is_deleted