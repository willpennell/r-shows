from pydantic import BaseModel, EmailStr

class RequestBody(BaseModel):
    email: EmailStr
    
class UpdatePasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    token: str