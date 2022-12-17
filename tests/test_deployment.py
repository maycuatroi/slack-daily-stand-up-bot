import uuid

import requests

BASE_ENDPOINT = "https://metax-daily-meeting-7xd5wwlzuq-uc.a.run.app"


def test_challenge():
    """
    Test challenge
    """
    challenge = uuid.uuid4().hex
    payload = {
        "challenge": challenge,
    }
    url = f"{BASE_ENDPOINT}/slack/events"

    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert response.json() == {"challenge": challenge}

if __name__ == '__main__':
    test_challenge()