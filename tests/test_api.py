import uuid
import sys

sys.path.append(".")
from http import client
from fastapi.testclient import TestClient

from main import app


def test_challenge():
    """
    Test challenge
    """
    challenge = uuid.uuid4().hex
    payload = {
        "challenge": challenge,
    }
    response = TestClient(app).post("/slack/events", json=payload)
    assert response.status_code == client.OK
    assert response.json() == {"challenge": challenge}
