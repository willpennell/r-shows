from fastapi import HTTPException
from app.db.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.schemas.refresh_token_schema import RefreshTokenData
from app.db.refresh_token_repository import RefreshTokenRepository

from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from app.config import SECRET_ACCESS_REFRESH_KEY
from app.models.user import User
import uuid

from datetime import datetime, timedelta

from loguru import logger as log

class RefreshTokenService:
    def __init__(self, user_repository: UserRepository, refresh_token_repository: RefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository
        self.user_repository = user_repository
        self.secret_key = SECRET_ACCESS_REFRESH_KEY
        self.algorithm = 'HS256'
        
        
    def refresh_access_token(self, refresh_token: str, user_id: str):
        log.info(f"Refresh token:  {refresh_token} \n In service")
        user_service = UserService(self.user_repository)
        auth_service = AuthService(self.user_repository)
        
        decoded_token = self.validate_refresh_token(refresh_token)
        
        user_id_from_sub = decoded_token["sub"]
        self.validate_user_id(user_id=user_id, sub=user_id_from_sub)
        
        user = user_service.get_user(user_id)
        
        
        new_access_token = auth_service.create_access_token(user)
        return new_access_token
    
        
    def validate_refresh_token(self, refresh_token: str):
        try:
            token_data = jwt.decode(refresh_token, self.secret_key, algorithms=self.algorithm)
            return token_data
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token has expired")
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    def validate_user_id(self, user_id, sub):
        if user_id != sub:
            raise HTTPException(status_code=401, detail="user ids do not match")
        
    def validate_token_exists(self, token: str):
        if self.refresh_token_repository.get_refresh_token(token) is None:
            raise HTTPException(status_code=404, detail="Token does not exist")
    
    def create_refresh_token(self, user: User):
        jti = str(uuid.uuid4())
        expiration_date = datetime.now() + timedelta(days=30)

        token_data = RefreshTokenData(
            sub=user.id,
            jti=jti,
            exp=expiration_date.timestamp()
        )
        log.info(f"Secret: {self.secret_key}")
        encoded_jwt  = jwt.encode(token_data.dict(), self.secret_key, algorithm=self.algorithm)
        self.refresh_token_repository.create_refresh_token(user.id, encoded_jwt, expiration_date)
        log.info(f"Encoded Refresh token {encoded_jwt}")
        
        token_data = jwt.decode(encoded_jwt, self.secret_key, algorithms=self.algorithm)
        log.debug(f"decoded jwt: {token_data}")
        return encoded_jwt