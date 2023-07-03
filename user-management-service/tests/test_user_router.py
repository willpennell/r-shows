from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_register_user_router():
    user_data = {
        "username": "johndoe123",
        "forenames": "John",
        "surname": "Doe",
        "email": "johndoe@example.com",
        "password": "password123"
    }

    response = client.post("users/register", json=user_data)

    assert response.status_code == 201
    assert response.json() == {
        "success": True,
        "response": {
            "userId": 1
        },
        "message": "User successfully created"
    }

def test_incorrect_email_format():
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

def test_empty_request_body():
    

    response = client.post("user/register")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
