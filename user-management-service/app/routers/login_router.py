from fastapi import APIRouter, Depends, HTTPException, status

from app.db.user_repository import UserRepository
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.email_service import EmailService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.login_service import LoginService
from app.schemas.auth_token_schema import AuthResponseBody
from app.database import get_db

from loguru import logger as log

router = APIRouter(
    tags=["login"]
)

@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db : Session=Depends(get_db)):
    log.info("In router")
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    auth_service = AuthService(user_repository)
    login_service = LoginService()
    
    
    access_token = login_service.login(form_data.username, form_data.password, user_service, auth_service)
    
    
    
    if access_token:
        response = AuthResponseBody(
            access_token=access_token,
            token_type="bearer"
        )
        return response