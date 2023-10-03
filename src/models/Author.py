class Author():

    def __init__(self, student_code, author_id, person_id):
        self.student_code = student_code
        self.author_id = author_id
        self.person_id = person_id

    def __init__(self, student_code, author_id, person_id, firstname, lastname, dni, phone, address, email, image, username, is_deleted=False):
        self.student_code = student_code
        self.author_id = author_id
        self.person_id = person_id
        self.firstname = firstname
        self.lastname = lastname
        self.dni = dni
        self.phone = phone
        self.address = address
        self.email = email
        self.image = image
        self.username = username
        self.is_deleted = is_deleted

