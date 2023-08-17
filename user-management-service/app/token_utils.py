import jwt
from app.config import SECRET_KEY_JWT
from datetime import datetime
from loguru import logger as log

def generate_reset_jwt(email: str, expiration: str):
    payload = {"email": email, "expiration": expiration}
    return jwt.encode(payload, SECRET_KEY_JWT, algorithm='HS256')

def decode_reset_token(token):
    try: 
        decoded_token = jwt.decode(token, SECRET_KEY_JWT, algorithms='HS256')
        
        email = decoded_token["email"]
        expiration = decoded_token["expiration"]
        
        current_time = datetime.utcnow()
        datetime_expiration = datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S")
        if current_time > datetime_expiration:
            log.info("token expired")
        else:
            log.info("Token is valid")
            log.info("Email: ", email)
            log.info("Expiration: ", expiration)
    except jwt.ExpiredSignatureError:
        log.info("Token has expired")
    except jwt.InvalidTokenError:
        log.info("Invalid Token")
        