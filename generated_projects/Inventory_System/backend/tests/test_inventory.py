"""
Inventory API Smoke Tests
"""


def test_inventory_get_all(client):

    response = client.get(
        "/inventorys/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_inventory_not_found(client):

    response = client.get(
        "/inventorys/999999"
    )

    assert response.status_code == 404
