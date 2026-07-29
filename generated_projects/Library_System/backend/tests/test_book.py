"""
Book API Smoke Tests
"""


def test_book_get_all(client):

    response = client.get(
        "/books/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_book_not_found(client):

    response = client.get(
        "/books/999999"
    )

    assert response.status_code == 404
