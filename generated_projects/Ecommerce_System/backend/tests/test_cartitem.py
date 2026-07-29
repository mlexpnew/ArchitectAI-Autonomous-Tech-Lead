"""
CartItem API Smoke Tests
"""


def test_cartitem_get_all(client):

    response = client.get(
        "/cartitems/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_cartitem_not_found(client):

    response = client.get(
        "/cartitems/999999"
    )

    assert response.status_code == 404
