"""
BorrowRecord API Smoke Tests
"""


def test_borrowrecord_get_all(client):

    response = client.get(
        "/borrowrecords/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_borrowrecord_not_found(client):

    response = client.get(
        "/borrowrecords/999999"
    )

    assert response.status_code == 404
