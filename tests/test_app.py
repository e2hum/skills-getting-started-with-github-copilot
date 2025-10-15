import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400


def test_unregister_participant():
    import uuid
    email = f"testuser_{uuid.uuid4()}@mergington.edu"
    activity = "Chess Club"
    # Check participants before
    before = client.get("/activities").json()[activity]["participants"]
    print(f"Before signup: {before}")
    # Sign up participant
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    # Check participants after signup
    after_signup = client.get("/activities").json()[activity]["participants"]
    print(f"After signup: {after_signup}")
    assert email in after_signup
    # Unregister the participant
    response = client.post(
        f"/activities/{activity}/unregister",
        json={"email": email},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    # Check participants after unregister
    after_unreg = client.get("/activities").json()[activity]["participants"]
    print(f"After unregister: {after_unreg}")
    assert email not in after_unreg


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister", json={"email": "test@mergington.edu"})
    assert response.status_code == 404
