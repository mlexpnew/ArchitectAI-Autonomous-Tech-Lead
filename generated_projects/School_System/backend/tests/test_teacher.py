"""
Teacher API Smoke Tests
"""


def test_teacher_get_all(client):

    response = client.get(
        "/teachers/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_teacher_not_found(client):

    response = client.get(
        "/teachers/999999"
    )

    assert response.status_code == 404
