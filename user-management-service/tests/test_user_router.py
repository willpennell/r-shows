from fastapi.testclient import TestClient
from app.main import app
from app.services.user_service import UserService
from app.database import get_db
from pytest_mock import mocker
from app.models.user import User
from app.schemas.user_schemas import UserRegistrationRequest
from app.password_utils import hash_password

client = TestClient(app)

def test_register_user_router(mocker):
    mock_user_service = mocker.Mock()
    app.dependency_overrides[get_db] = lambda: mocker.MagicMock()
    app.dependency_overrides[UserService] = lambda: mock_user_service
    user_data = {
        "username": "johndoe123",
        "forenames": "John",
        "surname": "Doe",
        "email": "johndoe@example.com",
        "password": "password123"
    }
    user = User(
        username=user_data["username"],
        forenames=user_data["forenames"],
        surname=user_data["surname"],
        email=user_data["email"],
        password_hash=hash_password(user_data["password"])
    )
    user.id = 1  # Set the 'id' attribute explicitly

    mock_user_service.create_user.side_effect = lambda req: user

    response = client.post("users/register", json=user_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["success"] is True
    assert response_data["response"]["user_id"] == user.id
    assert response_data["message"] == "User successfully created."

    mock_user_service.create_user.assert_called_once_with(UserRegistrationRequest(**user_data))

def test_incorrect_email_format(mocker):
    mock_user_service = mocker.Mock()
    app.dependency_overrides[get_db] = lambda: mocker.MagicMock()
    app.dependency_overrides[UserService] = lambda: mock_user_service

    user_data = {
        "username": "johndoe123",
        "forenames": "John",
        "surname": "Doe",
        "email": "johndoeatexample.com",
        "password": "password123"
    }

    response = client.post("users/register", json=user_data)

    assert response.status_code == 422

    assert response.json() == {
        "detail": [
        {
            "loc": [
                "body",
                "email"
            ],
            "msg": "value is not a valid email address",
            "type": "value_error.email"
        }
    ]}
    mock_user_service.create_user.assert_not_called()

def test_empty_request_body(mocker):
    mock_user_service = mocker.Mock()
    app.dependency_overrides[get_db] = lambda: mocker.MagicMock()
    app.dependency_overrides[UserService] = lambda: mock_user_service

    response = client.post("/users/register")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}
    mock_user_service.create_user.assert_not_called()