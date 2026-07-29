"""
Branch API Smoke Tests
"""


def test_branch_get_all(client):

    response = client.get(
        "/branchs/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_branch_not_found(client):

    response = client.get(
        "/branchs/999999"
    )

    assert response.status_code == 404
