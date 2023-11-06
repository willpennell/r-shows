from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.refresh_token_service import RefreshTokenService
from app.db.user_repository import UserRepository
from app.database import get_db
from app.password_utils import verify_password

from loguru import logger as log

class LoginService:
    
    def login(self, email: str, password: str, user_service: UserService, auth_service: AuthService, refresh_token_service: RefreshTokenService):
        
        # First Verify Username and Password
        log.info("in login method")
        user = user_service.get_user_by_email(email)
        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        # Generate new Refresh Token
        refresh_token = refresh_token_service.create_refresh_token(user)
        # Generate new Access Token
        access_token = auth_service.create_access_token(user)
        return access_token, refresh_token
    
    def verify_password(self, plain_password, hashed_password):
        return verify_password(plain_password, hashed_password)