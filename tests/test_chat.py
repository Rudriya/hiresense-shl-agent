from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_recommendation():

    payload = {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Hiring a mid-level "
                    "Java developer"
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

    assert "reply" in data

    assert "recommendations" in data

    assert isinstance(
        data["recommendations"],
        list
    )

    assert (
        data["end_of_conversation"]
        is True
    )