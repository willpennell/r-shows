from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from app.database import Base, get_db
from app.main import app
from app.models.user import User


@pytest.fixture(scope="module")
def test_client():


    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

    with TestClient(app) as client:
        yield client

    Base.metadata.drop_all(bind=engine)



def test_register_user(test_client):

    user_data = {
        "username": "johndoe123",
        "forenames": "John",
        "surname": "Doe",
        "email": "johndoe@example.com",
        "password": "password123"
    }

    response = test_client.post("/users/register", json=user_data)

    print("Response JSON:", response.json())


    assert response.status_code == 201
    assert response.json()["success"] == True
    assert response.json()["response"]["user_id"] == 1




