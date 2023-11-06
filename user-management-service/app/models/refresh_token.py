from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    refresh_token = Column(String(255), nullable=False)
    expiration = Column(DateTime(timezone=True))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    