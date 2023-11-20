from typing import List
from model import User

class UserRepository:
    def __init__(self):
        self.users = []

    def create_user(self, user: User):
        user.user_id = len(self.users) + 1
        self.users.append(user)
        return user

    def get_user(self, user_id: int):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None  

    def update_user(self, user_id: int, updated_user: User):
        for i, user in enumerate(self.users):
            if user.user_id == user_id:
                self.users[i] = updated_user
                return updated_user
        return None

    def delete_user(self, user_id: int):
        for i, user in enumerate(self.users):
            if user.user_id == user_id:
                deleted_user = self.users.pop(i)
                return deleted_user
        return None
    


