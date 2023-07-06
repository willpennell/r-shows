import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash_password.decode("utf-8")

def verify_password(entered_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(entered_password.encode("utf-8"), hashed_password.encode("utf-8"))
