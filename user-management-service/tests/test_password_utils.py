from app.password_utils import hash_password, verify_password


def test_hash_password_returns_str():
    password: str = "password1!"
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)

def test_verify_password_returns_true():
    password: str = "password1!"
    hashed_password: str = hash_password(password)
    assert verify_password(password, hashed_password) == True

def test_verify_password_returns_false():
    password: str = "password1!"
    hashed_password: str = hash_password(password)
    incorrect_password: str = "wrongpassword!"
    assert verify_password(incorrect_password, hashed_password) == False

def test_randomness_of_salt_in_hash_password():
    password1: str = "password1!"
    hashed_password1: str = hash_password(password1)
    
    password2: str = "password1!"
    hashed_password2: str = hash_password(password2)

    assert hashed_password1 != hashed_password2

def test_hash_password_with_empty_password():
    password = ""
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != ""

def test_hash_password_with_empty_password():
    password = ""
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != ""

def test_hash_password_with_empty_password():
    password = ""
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != ""

def test_hash_password_with_empty_password():
    password = ""
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != ""

def test_hash_password_max_length_password():
    password = "a" * 256
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
