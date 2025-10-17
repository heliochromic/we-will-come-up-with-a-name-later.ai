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
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
    response = requests.post(f"{BASE_URL}/api/transcripts/", json=payload, headers=headers)
    assert response.status_code == 201
    transcript = response.json()
    yield transcript
    requests.delete(f"{BASE_URL}/api/transcripts/{transcript['transcript_id']}", headers=headers)


def test_create_transcript(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
    response = requests.post(f"{BASE_URL}/api/transcripts/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert "transcript_id" in data
    assert "transcript_text" in data
    UUID(data["transcript_id"])


def test_get_transcript_by_id(auth_token, created_transcript):
    headers = {"Authorization": f"Bearer {auth_token}"}
    transcript_id = created_transcript["transcript_id"]
    response = requests.get(f"{BASE_URL}/api/transcripts/{transcript_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["transcript_id"] == transcript_id


def test_get_all_transcripts(auth_token, created_transcript):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/api/transcripts/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(t["transcript_id"] == created_transcript["transcript_id"] for t in data)


def test_delete_transcript(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    response = requests.post(f"{BASE_URL}/api/transcripts/", json=payload, headers=headers)
    assert response.status_code == 201
    transcript_id = response.json()["transcript_id"]

    response = requests.delete(f"{BASE_URL}/api/transcripts/{transcript_id}", headers=headers)
    assert response.status_code == 204

    response = requests.get(f"{BASE_URL}/api/transcripts/{transcript_id}", headers=headers)
    assert response.status_code == 404
