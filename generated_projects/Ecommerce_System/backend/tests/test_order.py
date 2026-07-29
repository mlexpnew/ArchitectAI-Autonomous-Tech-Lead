"""
Order API Smoke Tests
"""


def test_order_get_all(client):

    response = client.get(
        "/orders/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_order_not_found(client):

    response = client.get(
        "/orders/999999"
    )

    assert response.status_code == 404
