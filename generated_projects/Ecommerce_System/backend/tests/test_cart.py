"""
Cart API Smoke Tests
"""


def test_cart_get_all(client):

    response = client.get(
        "/carts/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_cart_not_found(client):

    response = client.get(
        "/carts/999999"
    )

    assert response.status_code == 404
