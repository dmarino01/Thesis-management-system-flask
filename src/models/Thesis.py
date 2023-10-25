class Thesis():
    def __init__(self, thesis_id, title, abstract, submission_date, pdf_link, thesis_status_id, is_deleted=False) -> None:
        self.thesis_id = thesis_id
        self.title = title
        self.abstract = abstract
        self.submission_date = submission_date
        self.pdf_link = pdf_link
        self.thesis_status_id = thesis_status_id
        self.is_deleted = is_deleted

    def __init__(self, thesis_id, title, abstract, submission_date, rating, pdf_link, thesis_status_id, author_id, firstname, lastname, is_deleted=False) -> None:
        self.thesis_id = thesis_id
        self.title = title
        self.abstract = abstract
        self.submission_date = submission_date
        self.rating = rating
        self.pdf_link = pdf_link
        self.thesis_status_id = thesis_status_id
        self.author_id = author_id
        self.firstname = firstname
        self.lastname = lastname
        self.is_deleted = is_deleted