# tests/test_main.py

import pytest
from app.main import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_shorten_and_redirect_flow(client):
    """Test the full flow: shortening a URL, then redirecting to it."""
    # 1. Shorten the URL
    long_url = "https://www.google.com/search?q=python"
    response = client.post("/api/shorten", json={"url": long_url})
    assert response.status_code == 201
    data = response.json
    assert "short_code" in data
    short_code = data["short_code"]
    assert len(short_code) == 6

    # 2. Use the short code to redirect
    redirect_response = client.get(f"/{short_code}")
    assert redirect_response.status_code == 302
    assert redirect_response.headers["Location"] == long_url

def test_get_stats(client):
    """Test the analytics endpoint after creating and using a short URL."""
    long_url = "https://github.com/features/copilot"
    
    # Create the short URL
    shorten_response = client.post("/api/shorten", json={"url": long_url})
    short_code = shorten_response.json["short_code"]

    # "Click" the link 3 times
    client.get(f"/{short_code}")
    client.get(f"/{short_code}")
    client.get(f"/{short_code}")

    # Get the stats
    stats_response = client.get(f"/api/stats/{short_code}")
    assert stats_response.status_code == 200
    stats_data = stats_response.json
    assert stats_data["url"] == long_url
    assert stats_data["clicks"] == 3
    assert "created_at" in stats_data

def test_shorten_invalid_url(client):
    """Test that the API returns a 400 error for an invalid URL."""
    response = client.post("/api/shorten", json={"url": "not-a-valid-url"})
    assert response.status_code == 400
    assert "error" in response.json

def test_redirect_not_found(client):
    """Test that accessing a non-existent short code returns a 404 error."""
    response = client.get("/nonexist")
    assert response.status_code == 404
    assert response.json == {"error": "Not Found"}

def test_stats_not_found(client):
    """Test that getting stats for a non-existent short code returns a 404 error."""
    response = client.get("/api/stats/nonexist")
    assert response.status_code == 404
    assert response.json == {"error": "Not Found"}