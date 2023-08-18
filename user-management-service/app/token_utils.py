import jwt
from app.config import SECRET_KEY_JWT
from datetime import datetime
from loguru import logger as log

def generate_reset_jwt(email: str, expiration: int):
    payload = {"email": email, "expiration": expiration}
    return jwt.encode(payload, SECRET_KEY_JWT, algorithm='HS256')

def decode_reset_token(token) -> bool:
    try: 
        decoded_token = jwt.decode(token, SECRET_KEY_JWT, algorithms='HS256')
        
        email = decoded_token["email"]
        expiration = decoded_token["expiration"]
        
        current_time = datetime.utcnow()
        
        if current_time.timestamp() > expiration:
            log.info("token expired")
            return False
        else:
            log.info("Token is valid")
            log.info(f"Email: {email}")
            log.info(f"Expiration: {expiration}")
            return True
    except jwt.ExpiredSignatureError:
        log.info("Token has expired")
    except jwt.InvalidTokenError:
        log.info("Invalid Token")
        