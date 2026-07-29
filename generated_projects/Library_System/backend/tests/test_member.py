"""
Member API Smoke Tests
"""


def test_member_get_all(client):

    response = client.get(
        "/members/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_member_not_found(client):

    response = client.get(
        "/members/999999"
    )

    assert response.status_code == 404
