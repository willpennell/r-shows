from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from app.db.user_repository import UserRepository
from app.services.user_service import UserService

from app.config import SECRET_ACCESS_KEY
from app.password_utils import verify_password
from app.schemas.auth_token_schema import JWTCredentials

from loguru import logger as log

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.secret_key = SECRET_ACCESS_KEY
        self.algorithm = "HS256"
        self.access_expire_time = 30
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        
    def verify_password(self, plain_password, hashed_password):
        return verify_password(plain_password, hashed_password)
    
    
    def create_access_token(self, data: JWTCredentials):
        to_encode = data.dict()
        encode_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        log.info(f"encoded jwt: {encode_jwt}")
        return encode_jwt
        
    def authenticate_user(self, email: str, password: str) -> JWTCredentials:
        user = self.user_repository.get_user_by_email(email)
        
        if not user or not self.verify_password(password, user.password_hash):
            return None
        
        access_token_expires = timedelta(minutes=self.access_expire_time)
        issued_at = datetime.utcnow()
        access_token_data = JWTCredentials(sub=user.id, email=user.email, exp=str(access_token_expires), iat=str(issued_at))
        log.info(f"access token data: {access_token_data}")
        access_token = self.create_access_token(access_token_data)
        log.info(f"Access Token: {access_token}")
        return access_token