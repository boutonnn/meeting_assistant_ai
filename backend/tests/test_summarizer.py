from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal, engine
from app.models.db_models import Base, MeetingInformation

import pytest
from unittest.mock import patch


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()


def test_upload_file(client, db):
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"Sample meeting content", "text/plain")},
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["filename"] == "test.txt"
    assert response_data["status"] == "pending"
    assert response_data["content"] == "Sample meeting content"

    # Verify database state
    summary_info = (
        db.query(MeetingInformation)
        .filter(MeetingInformation.id == response_data["id"])
        .first()
    )
    assert summary_info is not None
    assert summary_info.filename == "test.txt"


def test_upload_file_invalid_type(client):
    """Test uploading an invalid file type."""
    response = client.post(
        "/upload",
        files={"file": ("test.pdf", b"Invalid content", "application/pdf")},
    )
    assert response.status_code == 400
    assert (
        "Only .txt, .mp3, or .wav files are supported"
        in response.json()["detail"]
    )


def test_analyze_file_success(client, db):
    # First, upload a file
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"Test conversation", "text/plain")},
    )
    summary_id = response.json()["id"]

    # Mock OpenAI API response
    with patch("app.api.endpoints.generate_summary") as mock_summary:
        mock_summary.return_value = "Mocked summary: Key points discussed"
        response = client.post("/analyze", params={"id": summary_id})
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "completed"
        mock_summary.assert_called_once()
        assert (
            response_data["summary"] == "Mocked summary: Key points discussed"
        )

    # Verify database state
    summary_info = (
        db.query(MeetingInformation)
        .filter(MeetingInformation.id == summary_id)
        .first()
    )
    assert summary_info.status == "completed"
    assert summary_info.summary == "Mocked summary: Key points discussed"


def test_analyze_file_not_found(client):
    """Test analyzing a non-existent file."""
    response = client.post("/analyze", params={"id": 999})
    assert response.status_code == 404
    assert "Meeting information not found" in response.json()["detail"]


def test_get_results_success(client, db):
    """Test retrieving analysis results."""
    # Upload and analyze a file
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"Test conversation", "text/plain")},
    )
    assert response.status_code == 200
    summary_id = response.json()["id"]

    with patch("app.api.endpoints.generate_summary") as mock_summary:
        mock_summary.return_value = "Mocked summary: Key points discussed"
        response = client.post("/analyze", params={"id": summary_id})
        assert response.status_code == 200
        mock_summary.assert_called_once()

    # Retrieve results
    response = client.get(f"/results/{summary_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == summary_id
    assert response_data["filename"] == "test.txt"
    assert response_data["status"] == "completed"
    assert response_data["summary"] == "Mocked summary: Key points discussed"


def test_get_results_not_found(client):
    """Test retrieving results for a non-existent analysis."""
    response = client.get("/results/999")
    assert response.status_code == 404
    assert "Meeting information not found" in response.json()["detail"]
