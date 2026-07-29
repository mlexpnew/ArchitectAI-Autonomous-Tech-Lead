"""
Category API Smoke Tests
"""


def test_category_get_all(client):

    response = client.get(
        "/categorys/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_category_not_found(client):

    response = client.get(
        "/categorys/999999"
    )

    assert response.status_code == 404
