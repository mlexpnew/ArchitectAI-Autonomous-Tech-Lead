"""
OrderItem API Smoke Tests
"""


def test_orderitem_get_all(client):

    response = client.get(
        "/orderitems/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_orderitem_not_found(client):

    response = client.get(
        "/orderitems/999999"
    )

    assert response.status_code == 404
