from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.db.user_repository import UserRepository
from app.database import get_db

from loguru import logger as log

class LoginService:
        
        
    def login(self, email: str, password: str, user_service: UserService, auth_service: AuthService):
        log.info("in login method")
        
        access_token = auth_service.authenticate_user(email, password)
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        return access_token