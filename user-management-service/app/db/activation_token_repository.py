from sqlalchemy.orm import Session
from app.models.activation_token import ActivationToken
from sqlalchemy.exc import IntegrityError


class ActivationTokenRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_activation_token(self, activation_token: ActivationToken):
        try:
            self.db.add(activation_token)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Create not create token")
        
    def get_activation_token(self, activation_token: str) -> ActivationToken:
        return self.db.query(ActivationToken).filter(ActivationToken.token == activation_token).first()
    
    def get_activation_token_by_email(self, email: str) -> ActivationToken:
        return self.db.query(ActivationToken).filter(ActivationToken.email == email).first()
        
    
    def commit(self):
        self.db.commit()

    def refresh(self, obj):
        self.db.refresh(obj)