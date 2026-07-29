"""
Payment API Smoke Tests
"""


def test_payment_get_all(client):

    response = client.get(
        "/payments/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_payment_not_found(client):

    response = client.get(
        "/payments/999999"
    )

    assert response.status_code == 404
