"""
Doctor API Smoke Tests
"""


def test_doctor_get_all(client):

    response = client.get(
        "/doctors/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_doctor_not_found(client):

    response = client.get(
        "/doctors/999999"
    )

    assert response.status_code == 404
