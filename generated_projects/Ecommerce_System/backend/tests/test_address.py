"""
Address API Smoke Tests
"""


def test_address_get_all(client):

    response = client.get(
        "/addresss/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_address_not_found(client):

    response = client.get(
        "/addresss/999999"
    )

    assert response.status_code == 404
