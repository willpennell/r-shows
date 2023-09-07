
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models.refresh_token import RefreshToken

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_refresh_token(self, user_id: int, refresh_token: str, expiration: datetime):
        try:
            refresh_token_model = RefreshToken(
                user_id=user_id,
                refresh_token=refresh_token,
                expiration=expiration
            )
            self.db.add(refresh_token_model)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Could not create token")
    
    def get_refresh_token(self, token: str) -> RefreshToken:
        return self.db.query(RefreshToken).filter(RefreshToken.refresh_token == token).first()
    
    def get_refresh_token_by_user_id(self, user_id: str) -> RefreshToken:
        return self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()
    
    def delete_refresh_token(self, refresh_token: RefreshToken):
        self.db.delete(refresh_token)
    
    def commit(self):
        self.db.commit()
        
    def refresh(self, obj):
        self.db.refresh(obj)
            