"""
Staff API Smoke Tests
"""


def test_staff_get_all(client):

    response = client.get(
        "/staffs/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_staff_not_found(client):

    response = client.get(
        "/staffs/999999"
    )

    assert response.status_code == 404
