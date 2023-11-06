import jwt
from app.config import SECRET_KEY_RESET_JWT, SECRET_KEY_ACTIVATE_JWT
from datetime import datetime
from loguru import logger as log

def generate_reset_jwt(email: str, expiration: int):
    payload = {"email": email, "expiration": expiration}
    return jwt.encode(payload, SECRET_KEY_RESET_JWT, algorithm='HS256')



def decode_reset_token(token) -> bool:
    try: 
        decoded_token = jwt.decode(token, SECRET_KEY_RESET_JWT, algorithms='HS256')
        
        email = decoded_token["email"]
        expiration = decoded_token["expiration"]
        
        current_time = datetime.utcnow()
        
        if current_time.timestamp() > expiration:
            log.info("token expired")
            return False
        else:
            log.info("Token is valid")
            log.info(f"Email: {email}")
            log.info("Expiration: {expiration}")
            return True
    except jwt.ExpiredSignatureError:
        log.info("Token has expired")
    except jwt.InvalidTokenError:
        log.info("Invalid Token")

def generate_activation_jwt(user_id: int, email: str, expiration) -> str:
    payload = {"user_id": user_id, "email": email, "expiration": expiration}
    return jwt.encode(payload, SECRET_KEY_ACTIVATE_JWT, algorithm='HS256')

def decode_activate_token(token) -> (str, int):
    try: 
        decoded_token = jwt.decode(token, SECRET_KEY_ACTIVATE_JWT, algorithms='HS256')
        
        email = decoded_token["email"]
        expiration = decoded_token["expiration"]
        user_id = decoded_token["user_id"]
        
        current_time = datetime.utcnow()
        
        if current_time.timestamp() > expiration:
            log.info("token expired")
            raise jwt.InvalidTokenError
        return (email, user_id)
    except jwt.ExpiredSignatureError:
        log.info("Token has expired")
    except jwt.InvalidTokenError:
        log.info("Invalid Token")