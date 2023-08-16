from app.services.user_service import UserService
from app.db.user_repository import UserRepository
from app.db.password_token_repository import PasswordTokenRepository
from app.models.password_token import PasswordResetToken
from app.services.email_service import EmailService
from app.token_utils import generate_reset_jwt
from loguru import logger as loguru_logger
from datetime import datetime

class PasswordService:
    def __init__(self, token_repository: PasswordTokenRepository, user_repository: UserRepository):
        self.token_repository = token_repository
        self.user_repository = user_repository
        self.user_service = UserService(user_repository)
        self.email_service = EmailService()

    def generate_token(self, email: str) -> str:
        loguru_logger.info("In generate token service method.")
        if not self.user_service.user_email_exists(email):
            loguru_logger.error("Email not found")
            raise ValueError("Email not found")
        expiration = str(datetime.now())
        token = generate_reset_jwt(email, expiration)
        
        password_reset_token = PasswordResetToken(
            user_email=email,
            expiration=str(expiration),
            token=token
        )
        loguru_logger.info("password_reset_token: ", password_reset_token)
        
        self.token_repository.create_reset_token(password_reset_token)
        loguru_logger.info("token created")
        
        loguru_logger.info("Sending Email")
        self.email_service.send_email(email, token)
        loguru_logger.info("Sent!")