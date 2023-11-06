from fastapi import HTTPException
from app.schemas.user_schemas import UserRegistrationRequest, UserUpdateRequest, UserPartialUpdateRequest
from app.models.user import User
from sqlalchemy.orm import Session
from app.password_utils import hash_password
from app.token_utils import generate_activation_jwt, decode_activate_token
from app.db.user_repository import UserRepository
from app.db.activation_token_repository import ActivationTokenRepository
from app.models.activation_token import ActivationToken
from app.services.email_service import EmailService
from loguru import logger as log
from typing import Union
from datetime import datetime, timedelta

class UserService:
    def __init__(self, user_repository: UserRepository, activation_repository: Union[ActivationTokenRepository, None] = None, email_service: Union[EmailService, None] = None):
        self.user_repository = user_repository
        self.activation_repository = activation_repository
        self.email_service = email_service

    def create_user(self, user_data) -> User:
        user = User(
            username=user_data.username,
            forenames=user_data.forenames,
            surname=user_data.surname,
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )
        
        user = self.user_repository.create_user(user)
        self.generate_activation_token(user)
        
        return user
    

    def get_user(self, user_id: int) -> User:
        user = self.user_repository.get_user(user_id)
        return user
    
    def user_exists(self, user_id: int) -> bool:
        return self.user_repository.get_user(user_id) is not None
    
    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)
    
    def user_email_exists(self, email: str) -> bool:
        return self.user_repository.get_user_by_email(email) is not None
    
    def user_email_available(self, email: str) -> bool:
        return self.user_repository.get_user_by_email(email) is None
    
    def update_user(self, user_id: int, updated_user_data: UserUpdateRequest) -> User:
            if not self.user_exists(user_id):
                log.error("User not found")
                raise ValueError("User not found")
            
            
            
            log.debug("Updating user")
            user: User = self.user_repository.get_user(user_id)
            
            if user.active == False:
                log.error("User is not active")
                raise ValueError("User is not active")

            user.forenames = updated_user_data.forenames
            user.surname = updated_user_data.surname
            user.bio = updated_user_data.bio
            user.display_name = updated_user_data.display_name

            if self.user_email_exists(updated_user_data.email):
                log.error("Email already in use, bad request")
                raise ValueError("Email is already in use by another user.")
            
            user.email = updated_user_data.email

            
            self.user_repository.commit()
            self.user_repository.refresh(user)
            return user
            
        

    def partial_update_user(self, user_id: int, updated_user_data: UserPartialUpdateRequest) -> User:
        if not self.user_exists(user_id):
                log.error("User not found")
                raise ValueError("User not found")

        user: User = self.repository.get_user(user_id)
        
        if user.active == False:
                log.error("User is not active")
                raise ValueError("User is not active")
        
        if updated_user_data.forenames:
            user.forenames = updated_user_data.forenames

        if updated_user_data.surname:
            user.surname = updated_user_data.surname

        if updated_user_data.email and updated_user_data.email != user.email:
            if not self.user_repository.is_email_available(updated_user_data.email):
                log.error("Email already in use, bad request")
                raise ValueError("Email is already in use by another user.")
            user.email = updated_user_data.email
        
        if updated_user_data.bio:
            user.bio = updated_user_data.bio

        if updated_user_data.display_name:
            user.display_name = updated_user_data.display_name

        self.user_repository.commit()
        self.user_repository.refresh(user)
            
        return user
    
    def update_user_password(self, user_email, new_password) -> User:
        if not self.user_email_exists(user_email):
            log.error("User not found!")
            raise ValueError("User not found")
        
        user: User = self.get_user_by_email(user_email)
        
        user.password_hash = hash_password(new_password)
        
        self.user_repository.commit()
        self.user_repository.refresh(user)
        return user
    
    def activate_user(self, token: str):
        _, user_id = decode_activate_token(token)
        log.info(f"User ID: {user_id}")
        user = self.get_user(user_id)
        if user.active == False:
            log.info(f"User is active: {user.active}")
            user.active = True
        
        self.user_repository.commit()
        self.user_repository.refresh(user)
        return user
    
    def resend_activation(self, user):
        self.generate_activation_token(user)
    
    def generate_activation_token(self, user: User) -> User:
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(days=1)
        
        token = generate_activation_jwt(user.id, user.email, expiration_datetime.timestamp())
        activation_token = ActivationToken(
            user_email=user.email,
            user_id=user.id,
            token=token
        )
        
        self.activation_repository.create_activation_token(activation_token)
        
        self.email_service.send_email(user.email, self.email_service.activate_message(token), "Activate your account")
        return user 
    
    def deactivate_user(self, user: User) -> User:
        user.active = False
        self.user_repository.commit()
        self.user_repository.refresh(user)
        return user
        
    def delete_user(self, user: User) -> User:
        user.deleted = True
        
        self.user_repository.commit()
        self.user_repository.refresh(user)
        return user