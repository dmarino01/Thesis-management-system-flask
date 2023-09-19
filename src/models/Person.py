class Person():


    def __init__(self, firstname, lastname, phone, address, email, is_deleted=False):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.address = address
        self.email = email
        self.is_deleted = is_deleted