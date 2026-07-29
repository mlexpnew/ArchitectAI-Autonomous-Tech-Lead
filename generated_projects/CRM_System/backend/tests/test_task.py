"""
Task API Smoke Tests
"""


def test_task_get_all(client):

    response = client.get(
        "/tasks/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_task_not_found(client):

    response = client.get(
        "/tasks/999999"
    )

    assert response.status_code == 404
