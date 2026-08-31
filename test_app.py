"""
Basic tests, run automatically by the CI pipeline on every push.
Updated for the HTML landing page: "/" now serves HTML, "/api" serves JSON,
and "/health" is unchanged.
"""

from app import app


def test_home():
    """Home page returns the HTML landing page."""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    # The page is HTML and should contain our project title.
    assert b"Cloud DevOps Project" in response.data


def test_api():
    """The /api endpoint returns the JSON payload."""
    client = app.test_client()
    response = client.get("/api")
    assert response.status_code == 200
    assert "version" in response.get_json()


def test_health():
    """Health check endpoint returns healthy status (unchanged)."""
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"
