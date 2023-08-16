import jwt
from app.config import SECRET_KEY_JWT
from datetime import datetime

def generate_reset_jwt(email: str, expiration: str):
    payload = {"email": email, "expiration": expiration}
    return jwt.encode(payload, SECRET_KEY_JWT, algorithm='HS256')