import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

@pytest.fixture
def mock_unsplash():
    # Patch the functions in the 'main' module where they are imported
    with patch("main.get_unsplash_image") as mock_img, \
         patch("main.search_unsplash_images") as mock_search, \
         patch("main.generate_ai_caption") as mock_caption, \
         patch("main.extract_smart_keywords") as mock_keywords, \
         patch("main.generate_carousel_story") as mock_story:
        
        mock_img.return_value = {
            "url": "https://example.com/image.jpg",
            "credit": {"name": "Test User", "username": "test", "link": "https://unsplash.com/@test"}
        }
        mock_search.return_value = [
            {"url": "https://example.com/1.jpg", "credit": {"name": "User 1", "username": "u1", "link": "https://u1.com"}},
            {"url": "https://example.com/2.jpg", "credit": {"name": "User 2", "username": "u2", "link": "https://u2.com"}}
        ]
        mock_caption.return_value = "AI Generated Caption"
        mock_keywords.return_value = ["tech", "future", "clean"]
        mock_story.return_value = ["start", "middle", "end"]
        yield

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
    assert data["credit"]["name"] == "Test User"

def test_rate_limit():
    with patch("rate_limiter.rate_limiter.consume", return_value=False):
        response = client.get("/")
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()["detail"]

def test_security_api_key_leak(mock_unsplash):
    response = client.post("/social-media-post", json={"keyword": "nature", "platform": "instagram"})
    assert "Client-ID" not in response.text
    # Ensure no real keys leak in text
    assert "s8OgR_FRSMgGxxXnn9ba0J5iSPndfTj58zjvypdS8JI" not in response.text
