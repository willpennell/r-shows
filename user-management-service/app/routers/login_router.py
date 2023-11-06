from fastapi import APIRouter, Depends, HTTPException, status

from app.db.user_repository import UserRepository
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.email_service import EmailService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.db.refresh_token_repository import RefreshTokenRepository
from app.services.refresh_token_service import RefreshTokenService
from app.services.login_service import LoginService
from app.schemas.auth_token_schema import AuthResponseBody
from app.schemas.refresh_token_schema import RefreshTokenResponse
from app.schemas.login_schema import LoginResponse
from app.database import get_db

from loguru import logger as log

router = APIRouter(
    tags=["login"]
)

@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db : Session=Depends(get_db)):
    log.info("In router")
    user_repository = UserRepository(db)
    refresh_token_repository = RefreshTokenRepository(db)
    user_service = UserService(user_repository)
    auth_service = AuthService(user_repository)
    refresh_token_service = RefreshTokenService(user_repository, refresh_token_repository)
    login_service = LoginService()
    
    access_token, refresh_token = login_service.login(form_data.username, form_data.password, user_service, auth_service, refresh_token_service)
    
    if access_token:
        access_token_response = AuthResponseBody(
            access_token=access_token,
            token_type="bearer"
        )
        refresh_token_response = RefreshTokenResponse(
            refresh_token=refresh_token,
            token_type="refresh"
        )
        
        response = LoginResponse(
            access_response=access_token_response,
            refresh_response=refresh_token_response
        )
        return response