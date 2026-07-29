"""
Patient API Smoke Tests
"""


def test_patient_get_all(client):

    response = client.get(
        "/patients/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_patient_not_found(client):

    response = client.get(
        "/patients/999999"
    )

    assert response.status_code == 404
