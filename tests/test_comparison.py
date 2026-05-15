from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_comparison():

    payload = {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Compare OPQ and "
                    "Cognitive Assessments"
                )
            }
        ]
    }

    response = client.post(
        "/chat",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        "comparison"
        in data["reply"].lower()
        or "assessment"
        in data["reply"].lower()
    )