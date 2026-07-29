from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.user import User
from .schemas.user import UserSchema

class UserRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_user(self, user_id):
        session = self.Session()
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        return user

    def create_user(self, user: UserSchema):
        session = self.Session()
        new_user = User(
            username=user.username,
            password=user.password,
            role=user.role
        )
        session.add(new_user)
        session.commit()
        session.close()
        return new_user

    def update_user(self, user_id, user: UserSchema):
        session = self.Session()
        user_to_update = session.query(User).filter(User.id == user_id).first()
        if user_to_update:
            user_to_update.username = user.username
            user_to_update.password = user.password
            user_to_update.role = user.role
            session.commit()
            session.close()
            return user_to_update
        session.close()
        return None

    def delete_user(self, user_id):
        session = self.Session()
        user_to_delete = session.query(User).filter(User.id == user_id).first()
        if user_to_delete:
            session.delete(user_to_delete)
            session.commit()
            session.close()
            return True
        session.close()
        return False