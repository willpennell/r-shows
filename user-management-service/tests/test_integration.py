import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, test_engine, get_db, TestSessionLocal
from app.models.user import User
from app.schemas.user_schemas import UserRegistrationRequest
from app.services.user_service import UserService


@pytest.fixture(scope="module")
def test_app():
    # Create the necessary table(s)
    Base.metadata.create_all(bind=test_engine)

    # Bind the database to a session
    TestSessionLocal.configure(bind=test_engine)

    # Create the test client
    with TestClient(app) as client:
        yield client


async def test_register_user(test_app):
    # Test data
    user_data = {
        "username": "johndoe123",
        "forenames": "John",
        "surname": "Doe",
        "email": "johndoe@example.com",
        "password": "password123"
    }

    # Clear existing users
    with get_db(test_db=True) as db:
        db.query(User).delete()
        db.commit()

    # Create a user using the user service
    with get_db(test_db=True) as db:
        user_service = UserService(db)
        user = await user_service.create_user(UserRegistrationRequest(**user_data))

        # Make an HTTP request to the app's /users/register endpoint
        response = test_app.post("/users/register", json=user_data)

        # Assertions
        assert response.status_code == 201
        assert response.json()["username"] == user.username
        assert response.json()["email"] == user.email
