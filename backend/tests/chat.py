from html.parser import charref

import pytest
import requests
from uuid import UUID

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def user_data():
    return {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }
@pytest.fixture(scope="session")
def auth_token(user_data):
    """Отримуємо токен через логін"""
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/api/users/login", data=login_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    if response.status_code != 200:
        pytest.skip("Cannot obtain auth token from login")
    return response.json().get("access_token")


@pytest.fixture
def created_transcript(auth_token):
    """Створюємо тестовий транскрипт перед тестами і видаляємо після"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "video_url": "https://www.youtube.com/watch?v=dJYGatp4SvA&list=PL5-TkQAfAZFbzxjBHtzdVCWE0Zbhomg7r&index=1&t=12s"
    }
    response = requests.post(f"{BASE_URL}/api/transcripts/", json=payload, headers=headers)
    assert response.status_code == 201
    transcript = response.json()
    yield transcript
    # requests.delete(f"{BASE_URL}/api/transcripts/{transcript['transcript_id']}", headers=headers)

@pytest.fixture
def created_chat(auth_token, created_transcript):
    """Створюємо чат перед тестами і видаляємо після"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"transcript_id": created_transcript["transcript_id"]}
    response = requests.post(f"{BASE_URL}/api/chats/", json=payload, headers=headers)
    assert response.status_code == 201
    chat = response.json()
    yield chat
    requests.delete(f"{BASE_URL}/api/chats/{chat['chat_id']}", headers=headers)


def test_create_chat(auth_token, created_transcript):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"transcript_id": created_transcript["transcript_id"]}
    response = requests.post(f"{BASE_URL}/api/chats/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert "chat_id" in data
    assert data["transcript_id"] == created_transcript["transcript_id"]
    UUID(data["chat_id"])


def test_get_user_chats(auth_token, created_chat):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/api/chats/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(c["chat_id"] == created_chat["chat_id"] for c in data)


def test_get_chat_by_id(auth_token, created_chat):
    headers = {"Authorization": f"Bearer {auth_token}"}
    chat_id = created_chat["chat_id"]
    response = requests.get(f"{BASE_URL}/api/chats/{chat_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["chat_id"] == chat_id


def test_add_message(auth_token, created_chat):
    headers = {"Authorization": f"Bearer {auth_token}"}
    chat_id = created_chat["chat_id"]
    payload = {"sender": "user", "message_text": "Hello, AI!", "chat_id": chat_id}
    response = requests.post(f"{BASE_URL}/api/chats/{chat_id}/messages", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["sender"] == "user"
    assert data["message_text"] == "Hello, AI!"
    UUID(data["message_id"])


def test_get_chat_messages(auth_token, created_chat):
    headers = {"Authorization": f"Bearer {auth_token}"}
    chat_id = created_chat["chat_id"]
    response = requests.get(f"{BASE_URL}/api/chats/{chat_id}/messages", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("message_id" in msg for msg in data)


def test_send_message_to_llm(auth_token, created_chat):
    headers = {"Authorization": f"Bearer {auth_token}"}
    chat_id = created_chat["chat_id"]
    payload = {"user_message": "Explain this video", "provider": "openai", "chat_id": chat_id}
    response = requests.post(f"{BASE_URL}/api/chats/{chat_id}/llm", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["chat_id"] == chat_id
    assert "llm_message" in data
