import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

@pytest.fixture
def mock_unsplash():
    with patch("utils.requests.get") as mock_get:
        # Mocking a successful Unsplash response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "urls": {"regular": "https://example.com/image.jpg"},
            "user": {
                "name": "John Doe",
                "username": "johndoe",
                "links": {"html": "https://unsplash.com/@johndoe"}
            },
            "links": {"download_location": "https://api.unsplash.com/photos/123/download"},
            "results": [
                {
                    "urls": {"regular": "https://example.com/img1.jpg"},
                    "user": {"name": "User 1", "username": "u1", "links": {"html": "..."}},
                    "links": {"download_location": "..."}
                }
            ] * 5
        }
        mock_get.return_value = mock_response
        yield mock_get

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AxpostMedia API"}

def test_callback():
    response = client.get("/callback?code=testcode")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_social_media_post(mock_unsplash):
    response = client.post("/social-media-post", json={"keyword": "nature", "platform": "instagram"})
    assert response.status_code == 200
    data = response.json()
    assert "image_url" in data
    assert "caption" in data
    assert data["credit"]["name"] == "John Doe"

def test_rate_limit():
    # Since we set capacity=50 and fill_rate=50/3600, 
    # we can try to consume all tokens to test the limit.
    # But for a unit test, we might want to mock the rate limiter instead.
    with patch("rate_limiter.rate_limiter.consume", return_value=False):
        response = client.get("/")
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()["detail"]

def test_security_api_key_leak(mock_unsplash):
    # Ensure the access key is not in any response
    response = client.post("/social-media-post", json={"keyword": "nature", "platform": "instagram"})
    assert "Client-ID" not in response.text
    # Check that it's not in the credit links either (it shouldn't be)
    assert "your_access_key_here" not in response.text
