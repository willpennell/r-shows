import pytest
from app.schemas.user_schemas import UserRegistrationRequest
from app.models.user import User
from app.services.user_service import UserService
from pytest_mock import mocker
from pydantic import ValidationError
from app.db.user_repository import UserRepository


@pytest.fixture
def repository_mock(mocker):
    mock_repo = mocker.MagicMock(spec=UserRepository)
    mock_repo.create_user.side_effect = lambda user_data: User(
        username=user_data.username,
        forenames=user_data.forenames,
        surname=user_data.surname,
        email=user_data.email,
        password_hash="hashed_password"
    )
    def get_user_by_id(user_id):
        if user_id == 1:  
            return User(
                id=1,
                username="johndoe123",
                forenames="John",
                surname="Doe",
                email="john@example.com",
                password_hash="hashed_password"
            )
        return None
    
    mock_repo.get_user.side_effect = get_user_by_id
    return mock_repo



@pytest.fixture
def user_data():
    return UserRegistrationRequest(
            username="johndoe123",
            forenames="John",
            surname="Doe",
            email="john@example.com",
            password="password123"
        )

def test_create_user(repository_mock, user_data):

    service = UserService(repository=repository_mock)

    user = service.create_user(user_data)

    assert isinstance(user, User)
    assert user.username == user_data.username
    assert user.forenames == user_data.forenames
    assert user.surname == user_data.surname
    assert user.email == user_data.email


def test_empty_user_data_to_create_user(repository_mock):
    service = UserService(repository=repository_mock)
    with pytest.raises(ValidationError):
        service.create_user(UserRegistrationRequest())


def test_get_user_by_id(repository_mock, user_data):
    user_id = 1
    service = UserService(repository=repository_mock)
    
    user = service.get_user(user_id)
    
    assert isinstance(user, User)
    assert user.username == user_data.username
    assert user.forenames == user_data.forenames
    assert user.surname == user_data.surname
    assert user.email == user_data.email

