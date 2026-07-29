"""
Transaction API Smoke Tests
"""


def test_transaction_get_all(client):

    response = client.get(
        "/transactions/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_transaction_not_found(client):

    response = client.get(
        "/transactions/999999"
    )

    assert response.status_code == 404
