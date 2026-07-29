"""
Guest API Smoke Tests
"""


def test_guest_get_all(client):

    response = client.get(
        "/guests/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_guest_not_found(client):

    response = client.get(
        "/guests/999999"
    )

    assert response.status_code == 404
