"""
Warehouse API Smoke Tests
"""


def test_warehouse_get_all(client):

    response = client.get(
        "/warehouses/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_warehouse_not_found(client):

    response = client.get(
        "/warehouses/999999"
    )

    assert response.status_code == 404
