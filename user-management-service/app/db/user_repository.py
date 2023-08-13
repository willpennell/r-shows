from sqlalchemy.orm import Session
from app.models.user import User
from app.password_utils import hash_password

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
        
        self.db.add(user)
        self.db.commit()
    
        return user
    
    def get_user(self, user_id) -> User:
        print("In user repo: ", user_id)
        return self.db.query(User).filter(User.id == user_id).first()
    
    def is_email_available(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email).first() is None
    
    def commit(self):
        self.db.commit()

    def refresh(self, obj):
        self.db.refresh(obj)