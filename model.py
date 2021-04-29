class User:
    def __init__(self, id, username, password, authenticated, active):
        self.id = id
        self.username = username
        self.password = password
        self.active = active
        self.authenticated = authenticated

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_Name(self):
        return self.username

    def get_id(self):
        return self.id

    def get(self):
        return self
