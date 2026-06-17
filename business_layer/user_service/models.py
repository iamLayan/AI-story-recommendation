class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password  # لاحقًا يمكن تشفيره

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
