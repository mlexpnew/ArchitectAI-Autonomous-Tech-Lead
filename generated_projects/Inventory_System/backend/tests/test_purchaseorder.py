"""
PurchaseOrder API Smoke Tests
"""


def test_purchaseorder_get_all(client):

    response = client.get(
        "/purchaseorders/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_purchaseorder_not_found(client):

    response = client.get(
        "/purchaseorders/999999"
    )

    assert response.status_code == 404
