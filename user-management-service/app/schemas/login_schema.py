from pydantic import BaseModel
from datetime import datetime
from app.schemas.auth_token_schema import AuthResponseBody
from app.schemas.refresh_token_schema import RefreshTokenResponse

class LoginResponse(BaseModel):
    access_response: AuthResponseBody
    refresh_response: RefreshTokenResponse