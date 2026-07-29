"""
Product API Smoke Tests
"""


def test_product_get_all(client):

    response = client.get(
        "/products/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_product_not_found(client):

    response = client.get(
        "/products/999999"
    )

    assert response.status_code == 404
