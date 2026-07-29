"""
Supplier API Smoke Tests
"""


def test_supplier_get_all(client):

    response = client.get(
        "/suppliers/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_supplier_not_found(client):

    response = client.get(
        "/suppliers/999999"
    )

    assert response.status_code == 404
