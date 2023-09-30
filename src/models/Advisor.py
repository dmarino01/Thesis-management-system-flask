class Advisor():

    def __init__(self, advisor_code, institution, person_id, advisor_id):
        self.advisor_code = advisor_code
        self.institution = institution
        self.person_id = person_id
        self.advisor_id = advisor_id

    def __init__(self, advisor_code, institution, person_id, advisor_id, firstname, lastname, dni, phone, address, email, is_deleted=False):
        self.advisor_code = advisor_code
        self.institution = institution
        self.person_id = person_id
        self.advisor_id = advisor_id
        self.firstname = firstname
        self.lastname = lastname
        self.dni = dni
        self.phone = phone
        self.address = address
        self.email = email
        self.is_deleted = is_deleted