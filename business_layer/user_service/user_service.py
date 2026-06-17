from data_layer.database_handler import DatabaseHandlerSingleton
from .models import User
import json

USERS_FILE = "data_layer/users_data.json"

class UserService:
    def __init__(self):
        self.db = DatabaseHandlerSingleton()
        self.users = self.db.read_data(USERS_FILE)

    def register_user(self, username, email, password):
        # تحقق من عدم تكرار البريد أو اسم المستخدم
        if any(u["email"] == email for u in self.users):
            return None
        new_id = len(self.users) + 1
        new_user = User(new_id, username, email, password)
        self.users.append(new_user.to_dict())
        self.db.write_data(USERS_FILE, self.users)
        return new_user.to_dict()

    def login_user(self, email, password):
        user = next((u for u in self.users if u["email"] == email and u["password"] == password), None)
        return user

    def get_user(self, user_id):
        return next((u for u in self.users if u["user_id"] == user_id), None)
