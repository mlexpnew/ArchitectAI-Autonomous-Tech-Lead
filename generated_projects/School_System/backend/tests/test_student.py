"""
Student API Smoke Tests
"""


def test_student_get_all(client):

    response = client.get(
        "/students/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_student_not_found(client):

    response = client.get(
        "/students/999999"
    )

    assert response.status_code == 404
