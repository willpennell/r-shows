from app.services.user_service import UserService
from app.db.user_repository import UserRepository
from loguru import logger as loguru_logger

class PasswordService:
    def __init__(self, token_repository: TokenRepository, user_repository: UserRepository):
        self.token_repository = token_repository
        self.user_repository = user_repository
        self.user_service = UserService(user_repository)

    def generate_token(self, email: str) -> str:
        if not self.user_service.user_email_exists(email):
            loguru_logger.error("Email not found")
            raise ValueError("Email not found")
        
        # TODO Generate token