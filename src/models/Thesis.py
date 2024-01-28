class Thesis:
    def __init__(
        self,
        thesis_id,
        title,
        abstract,
        submission_date,
        expiration_date,
        last_update_date,
        rating,
        pdf_link,
        thesis_status_id,
        is_deleted=False,
    ) -> None:
        self.thesis_id = thesis_id
        self.title = title
        self.abstract = abstract
        self.submission_date = submission_date
        self.expiration_date = expiration_date
        self.last_update_date = last_update_date
        self.rating = rating
        self.pdf_link = pdf_link
        self.thesis_status_id = thesis_status_id
        self.is_deleted = is_deleted

    def __init__(
        self,
        thesis_id,
        title,
        abstract,
        submission_date,
        expiration_date,
        last_update_date,
        rating,
        pdf_link,
        turnitin_porcentaje,
        turnitin_link,
        article_link,
        thesis_status_id,
        project_id,
        mention_id,
        mention,
        author_id,
        firstname,
        lastname,
        is_deleted=False,
    ) -> None:
        self.thesis_id = thesis_id
        self.title = title
        self.abstract = abstract
        self.submission_date = submission_date
        self.expiration_date = expiration_date
        self.last_update_date = last_update_date
        self.rating = rating
        self.pdf_link = pdf_link
        self.turnitin_porcentaje = turnitin_porcentaje
        self.turnitin_link = turnitin_link
        self.article_link = article_link
        self.thesis_status_id = thesis_status_id
        self.project_id = project_id
        self.mention_id = mention_id
        self.mention = mention
        self.author_id = author_id
        self.firstname = firstname
        self.lastname = lastname
        self.is_deleted = is_deleted
