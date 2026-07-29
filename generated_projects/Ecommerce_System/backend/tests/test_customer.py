"""
Customer API Smoke Tests
"""


def test_customer_get_all(client):

    response = client.get(
        "/customers/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_customer_not_found(client):

    response = client.get(
        "/customers/999999"
    )

    assert response.status_code == 404
