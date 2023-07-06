from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    user_id : int
    username : str
    forenames: str
    surname : str
    email : EmailStr
    bio : Optional[str]
    display_name : str
    created_at:  datetime

class UserRegistrationRequest(BaseModel):
    username : str
    forenames: str
    surname: str
    email: EmailStr
    password: str
