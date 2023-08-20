from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base

class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'

    id = Column(Integer, primary_key=True)
    user_email = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False)
    expiration = Column(DateTime(timezone=True), default=func.now() + func.interval('30 minutes'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())