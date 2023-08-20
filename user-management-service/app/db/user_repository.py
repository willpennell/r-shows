from sqlalchemy.orm import Session
from app.models.user import User
from app.password_utils import hash_password
from sqlalchemy.exc import IntegrityError

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: User) -> User:
        
        try: 
            self.db.add(user_data)
            self.db.commit()
            return user_data
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