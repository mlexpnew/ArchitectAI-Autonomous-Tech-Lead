"""
Reservation API Smoke Tests
"""


def test_reservation_get_all(client):

    response = client.get(
        "/reservations/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_reservation_not_found(client):

    response = client.get(
        "/reservations/999999"
    )

    assert response.status_code == 404
