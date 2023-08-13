from app.schemas.user_schemas import UserRegistrationRequest, UserUpdateRequest, UserPartialUpdateRequest
from app.models.user import User
from sqlalchemy.orm import Session
from app.password_utils import hash_password
from app.db.user_repository import UserRepository
from loguru import logger as loguru_logger

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data):
        return self.repository.create_user(user_data)
        
    def get_user(self, user_id):
        return self.repository.get_user(user_id)
    
    def update_user(self, user_id: int, updated_user_data: UserUpdateRequest) -> User:
        
            loguru_logger.debug("In update_user()")
            user: User = self.repository.get_user(user_id)

            user.forenames = updated_user_data.forenames
            user.surname = updated_user_data.surname
            user.bio = updated_user_data.bio
            user.display_name = updated_user_data.display_name

            if not self.repository.is_email_available(updated_user_data.email):
                loguru_logger.error("Email already in use, bad request")
                raise ValueError("Email is already in use by another user.")
            user.email = updated_user_data.email

            self.repository.commit()
            self.repository.refresh(user)
                
            return user
        

    def partial_update_user(self, user_id: int, updated_user_data: UserPartialUpdateRequest) -> User:
        user: User = self.repository.get_user(user_id)

        if updated_user_data.forenames:
            user.forenames = updated_user_data.forenames

        if updated_user_data.surname:
            user.surname = updated_user_data.surname

        if updated_user_data.email and updated_user_data.email != user.email:
            if not self.repository.is_email_available(updated_user_data.email):
                loguru_logger.error("Email already in use, bad request")
                raise ValueError("Email is already in use by another user.")
            user.email = updated_user_data.email
        
        if updated_user_data.bio:
            user.bio = updated_user_data.bio

        if updated_user_data.display_name:
            user.display_name = updated_user_data.display_name

        self.repository.commit()
        self.repository.refresh(user)
            
        return user