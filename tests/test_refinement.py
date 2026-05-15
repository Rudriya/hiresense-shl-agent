from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_refinement():

    payload = {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Hiring a Java developer"
                )
            },
            {
                "role": "assistant",
                "content": (
                    "What seniority level "
                    "are you hiring for?"
                )
            },
            {
                "role": "user",
                "content": (
                    "Mid-level. "
                    "Also add personality tests."
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
        len(data["recommendations"]) > 0
    )