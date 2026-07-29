"""
Enrollment API Smoke Tests
"""


def test_enrollment_get_all(client):

    response = client.get(
        "/enrollments/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_enrollment_not_found(client):

    response = client.get(
        "/enrollments/999999"
    )

    assert response.status_code == 404
