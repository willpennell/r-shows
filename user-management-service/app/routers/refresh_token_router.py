from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.user_schemas import UserRegistrationRequest, UserUpdateRequest, UserPartialUpdateRequest
from app.services.user_service import UserService
from app.schemas.response_schema import ResponseBody
from app.schemas.activation_token_schema import RequestBody as ActivationRequest
from app.db.activation_token_repository import ActivationTokenRepository
from app.services.email_service import EmailService
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from loguru import logger as log
from fastapi.security import OAuth2PasswordBearer
from app.schemas.refresh_token_schema import RefreshTokenData
from app.schemas.auth_token_schema import AuthResponseBody
from app.services.auth_service import AuthService
from app.db.user_repository import UserRepository
from app.schemas.auth_token_schema import JWTCredentials
from app.services.refresh_token_service import RefreshTokenService
from app.schemas.refresh_token_schema import RefreshAccessTokenRequest
from app.db.refresh_token_repository import RefreshTokenRepository
from loguru import logger as log



router = APIRouter(
    tags=["refresh_token"]
)


@router.post("/new-access-token", status_code=status.HTTP_200_OK)
def refresh_access_token(token: RefreshAccessTokenRequest, db : Session = Depends(get_db)):
    log.info("In refresh router")
    user_repository = UserRepository(db)
    refresh_token_repository = RefreshTokenRepository(db)
    refresh_token_service = RefreshTokenService(user_repository, refresh_token_repository)
    
    new_access_token = refresh_token_service.refresh_access_token(token.refresh_token, token.user_id)
    
    response = AuthResponseBody(
        access_token=new_access_token,
        token_type="bearer"
    )
    
    return response