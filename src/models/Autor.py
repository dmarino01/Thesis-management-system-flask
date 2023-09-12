class Autor:
    # Define the Author model
    #id = db.Column(db.Integer, primary_key=True)
    #firstname = db.Column(db.String(50))
    #lastname = db.Column(db.String(50))
    #email = db.Column(db.String(100), unique=True)
    #phone = db.Column(db.String(255))
    #is_deleted = db.Column(db.Boolean, default=False)  # Field for logic deletion

    def __init__(self, id, firstname, lastname, email, phone):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.is_deleted = False
