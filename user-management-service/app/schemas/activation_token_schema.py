from pydantic import BaseModel, EmailStr

class RequestBody(BaseModel):
    email: EmailStr