"""
Card API Smoke Tests
"""


def test_card_get_all(client):

    response = client.get(
        "/cards/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_card_not_found(client):

    response = client.get(
        "/cards/999999"
    )

    assert response.status_code == 404
