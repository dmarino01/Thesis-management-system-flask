class Author():

    def __init__(self, student_code, author_id, person_id, firstname, lastname, phone, address, email, is_deleted=False):
        self.student_code = student_code
        self.author_id = author_id
        self.person_id = person_id
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.address = address
        self.email = email
        self.is_deleted = is_deleted


