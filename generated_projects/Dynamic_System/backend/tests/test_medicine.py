"""
Medicine API Smoke Tests
"""


def test_medicine_get_all(client):

    response = client.get(
        "/medicines/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_medicine_not_found(client):

    response = client.get(
        "/medicines/999999"
    )

    assert response.status_code == 404
