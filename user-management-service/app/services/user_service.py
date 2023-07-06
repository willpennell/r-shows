from app.schemas.user_schemas import UserRegistrationRequest
from app.models.user import User
from sqlalchemy.orm import Session
from app.password_utils import hash_password

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserRegistrationRequest) -> User:
        user = User(
            username=user_data.username,
            forenames=user_data.forenames,
            surname=user_data.surname,
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user