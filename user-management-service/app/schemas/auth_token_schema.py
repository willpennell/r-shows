from pydantic import BaseModel
from datetime import datetime

class JWTCredentials(BaseModel):
    sub: int
    email: str
    exp: str
    iat: str
    
class AuthResponseBody(BaseModel):
    access_token: str
    token_type: str