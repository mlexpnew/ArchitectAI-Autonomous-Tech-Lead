from .repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db_url):
        self.user_repository = UserRepository(db_url)

    def get_user(self, user_id):
        return self.user_repository.get_user(user_id)

    def create_user(self, user: dict):
        user_schema = UserSchema(**user)
        return self.user_repository.create_user(user_schema)

    def update_user(self, user_id, user: dict):
        user_schema = UserSchema(**user)
        return self.user_repository.update_user(user_id, user_schema)

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)