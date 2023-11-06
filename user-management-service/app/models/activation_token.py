from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean
from app.database import Base

class ActivationToken(Base):
    __tablename__ = 'user_activation_tokens'
    
    id = Column(Integer, primary_key=True)
    user_email = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
    token = Column(String(255), nullable=False)
    expiration = Column(DateTime(timezone=True))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    