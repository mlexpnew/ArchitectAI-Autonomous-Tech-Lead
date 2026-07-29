"""
Course API Smoke Tests
"""


def test_course_get_all(client):

    response = client.get(
        "/courses/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_course_not_found(client):

    response = client.get(
        "/courses/999999"
    )

    assert response.status_code == 404
