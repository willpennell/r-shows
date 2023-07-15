import pytest
from app.schemas.user_schemas import UserRegistrationRequest
from app.models.user import User
from app.services.user_service import UserService
from pytest_mock import mocker
from pydantic import ValidationError


@pytest.fixture
def db(mocker):
    mock_db = mocker.Mock()
    return mock_db

@pytest.fixture
def user_data():
    return UserRegistrationRequest(
            username="johndoe123",
            forenames="John",
            surname="Doe",
            email="john@example.com",
            password="password123"
        )

def test_create_user(db, user_data):

    service = UserService(db)

    user = service.create_user(user_data)

    assert isinstance(user, User)
    assert user.username == user_data.username
    assert user.forenames == user_data.forenames
    assert user.surname == user_data.surname
    assert user.email == user_data.email

def test_that_create_user_calls_add_to_db(db, user_data):
    service = UserService(db)

    db.add.reset_mock()

    user = service.create_user(user_data)

    assert db.add.called

def test_that_create_user_calls_commit_to_db(db, user_data):
    service = UserService(db)
    user = service.create_user(user_data)

    db.commit.reset_mock()
    assert db.add.commit


def test_that_create_user_calls_refresh_to_db(db, user_data):
    service = UserService(db)
    user = service.create_user(user_data)

    assert db.add.refresh

def test_empty_user_data_to_create_user():
    service = UserService(db)
    with pytest.raises(ValidationError):
        service.create_user(UserRegistrationRequest())