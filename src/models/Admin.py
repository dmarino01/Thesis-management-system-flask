class Admin():

    def __init__(self, person_id, firstname, lastname, dni, phone, address, email, image, username, is_deleted=False):
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