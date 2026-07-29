"""
Appointment API Smoke Tests
"""


def test_appointment_get_all(client):

    response = client.get(
        "/appointments/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_appointment_not_found(client):

    response = client.get(
        "/appointments/999999"
    )

    assert response.status_code == 404
