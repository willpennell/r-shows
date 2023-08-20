from sqlalchemy.orm import Session
from app.models.password_token import PasswordResetToken
from sqlalchemy.exc import IntegrityError

class PasswordTokenRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_reset_token(self, password_token: PasswordResetToken):
        try:
            self.db.add(password_token)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Could not create token")
        
    def get_reset_token(self, token: str) -> PasswordResetToken:
        return self.db.query(PasswordResetToken).get(token)
    
    def commit(self):
        self.db.commit()

    def refresh(self, obj):
        self.db.refresh(obj)