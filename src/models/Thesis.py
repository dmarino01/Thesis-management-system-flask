class Thesis():
    def __init__(self, thesis_id, title, abstract, submission_date, thesis_status_id, is_deleted=False) -> None:
        self.thesis_id = thesis_id
        self.title = title
        self.abstract = abstract
        self.submission_date = submission_date
        self.thesis_status_id = thesis_status_id
        self.is_deleted = is_deleted