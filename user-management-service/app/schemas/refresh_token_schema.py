from pydantic import BaseModel

class RefreshTokenData(BaseModel):
    sub: int
    jti: str
    exp: int

class RefreshTokenResponse(BaseModel):
    refresh_token: str
    token_type: str
    
class RefreshAccessTokenRequest(BaseModel):
    refresh_token: str
    user_id: int