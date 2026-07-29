"""
Account API Smoke Tests
"""


def test_account_get_all(client):

    response = client.get(
        "/accounts/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_account_not_found(client):

    response = client.get(
        "/accounts/999999"
    )

    assert response.status_code == 404
