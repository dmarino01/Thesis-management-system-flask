class Permission():

    def __init__(self, permission_id, permission, description, is_deleted=False):
        self.permission_id = permission_id
        self.permission = permission
        self.description = description
        self.is_deleted = is_deleted