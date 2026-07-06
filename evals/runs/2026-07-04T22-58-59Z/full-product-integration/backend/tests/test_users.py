from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_users() -> None:
    response = client.get("/api/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1
    assert "id" in users[0]
    assert "email" in users[0]
