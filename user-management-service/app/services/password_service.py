from app.services.user_service import UserService
from app.db.user_repository import UserRepository
from app.db.password_token_repository import PasswordTokenRepository
from app.models.password_token import PasswordResetToken
from app.services.email_service import EmailService
from app.token_utils import generate_reset_jwt, decode_reset_token
from loguru import logger as log
from datetime import datetime, timedelta
import smtplib
class PasswordService:
    def __init__(self, token_repository: PasswordTokenRepository, user_repository: UserRepository):
        self.token_repository = token_repository
        self.user_repository = user_repository
        self.user_service = UserService(user_repository)
        self.email_service = EmailService()

    def generate_token(self, email: str) -> str:
        log.info("In generate token service method.")
        if not self.user_service.user_email_exists(email):
            log.error("Email not found")
            raise ValueError("Email not found")
        current_datetime = datetime.now()
        expiration = current_datetime + timedelta(minutes=30)
        
        token = generate_reset_jwt(email, expiration.timestamp())
        
        password_reset_token = PasswordResetToken(
            user_email=email,
            expiration=expiration,
            token=token
        )
        log.info("password_reset_token: ", password_reset_token)
        
        self.token_repository.create_reset_token(password_reset_token)
        log.info("token created")
        
        log.info("Sending Email")
        self.email_service.send_email(email, self.email_service.reset_message(token), "Reset Token")
        log.info("Sent!")
        
    def verify_reset_token(self, reset_token: str) -> bool:
        if decode_reset_token(reset_token) and self.reset_token_exists(reset_token):
            return True
        return False
        
    def reset_token_exists(self, token: str) -> bool:
        return self.token_repository.get_reset_token(token) is not None