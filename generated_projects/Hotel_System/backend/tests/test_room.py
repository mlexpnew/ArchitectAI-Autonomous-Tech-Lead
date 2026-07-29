"""
Room API Smoke Tests
"""


def test_room_get_all(client):

    response = client.get(
        "/rooms/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_room_not_found(client):

    response = client.get(
        "/rooms/999999"
    )

    assert response.status_code == 404
