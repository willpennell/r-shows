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
    display_name : Optional[str]
    created_at:  datetime

class UserRegistrationRequest(BaseModel):
    username : str
    forenames: str
    surname: str
    email: EmailStr
    password: str

class UserUpdateRequest(BaseModel):
    forenames: str
    surname : str
    email : EmailStr
    bio : str
    display_name : str


class UserPartialUpdateRequest(BaseModel):
    forenames: Optional[str]
    surname : Optional[str]
    email : Optional[EmailStr]
    bio : Optional[str]
    display_name : Optional[str]

    class Config:
        extra = "forbid"