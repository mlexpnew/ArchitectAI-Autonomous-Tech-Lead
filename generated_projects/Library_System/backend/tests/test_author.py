"""
Author API Smoke Tests
"""


def test_author_get_all(client):

    response = client.get(
        "/authors/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_author_not_found(client):

    response = client.get(
        "/authors/999999"
    )

    assert response.status_code == 404
