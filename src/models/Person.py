import base64

class Person():

    def __init__(self, firstname, lastname, dni, phone, address, email, image, is_deleted=False):
        self.firstname = firstname
        self.lastname = lastname
        self.dni = dni
        self.phone = phone
        self.address = address
        self.email = email
        self.image = image
        self.is_deleted = is_deleted