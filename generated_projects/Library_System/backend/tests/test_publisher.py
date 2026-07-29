"""
Publisher API Smoke Tests
"""


def test_publisher_get_all(client):

    response = client.get(
        "/publishers/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_publisher_not_found(client):

    response = client.get(
        "/publishers/999999"
    )

    assert response.status_code == 404
