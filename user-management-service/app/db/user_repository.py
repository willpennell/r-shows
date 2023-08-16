from sqlalchemy.orm import Session
from app.models.user import User
from app.password_utils import hash_password
from sqlalchemy.exc import IntegrityError

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data) -> User:
        user = User(
            username=user_data.username,
            forenames=user_data.forenames,
            surname=user_data.surname,
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )
        try: 
            self.db.add(user)
            self.db.commit()
            return user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Username or email already exists")
    
    def get_user(self, user_id) -> User:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
    
    
    def commit(self):
        self.db.commit()

    def refresh(self, obj):
        self.db.refresh(obj)