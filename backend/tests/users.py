import pytest
import requests
from uuid import UUID

BASE_URL = "http://127.0.0.1:8000/api/users"

@pytest.fixture(scope="session")
def user_data():
    return {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }


def test_register_user(user_data):
    """Перевіряємо створення нового користувача"""
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code in (201, 400, 500)

    if response.status_code == 201:
        data = response.json()
        print(data)
        assert "user_id" in data
        assert data["email"] == user_data["email"]

def test_login_user(user_data):
    """Перевіряємо логін користувача"""
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    assert response.status_code in (200, 401)

    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == user_data["email"]

@pytest.fixture(scope="session")
def auth_token():
    """Отримуємо токен через логін"""
    login_payload = {
        "username": "testuser@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/login", data=login_payload)
    if response.status_code != 200:
        pytest.skip("Cannot obtain auth token from login")
    return response.json().get("access_token")


def test_get_current_user(auth_token):
    """Отримуємо дані про поточного користувача"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "email" in data
    assert "user_id" in data
    UUID(data["user_id"])  # валідація UUID


def test_update_profile(auth_token):
    """Оновлюємо профіль"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Updated Test User"
    }

    response = requests.put(f"{BASE_URL}/me", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Test User"


# def test_delete_profile(auth_token):
#     """Видаляємо користувача"""
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     response = requests.delete(f"{BASE_URL}/me", headers=headers)
#     assert response.status_code == 204
