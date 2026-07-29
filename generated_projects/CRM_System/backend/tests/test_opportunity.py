"""
Opportunity API Smoke Tests
"""


def test_opportunity_get_all(client):

    response = client.get(
        "/opportunitys/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_opportunity_not_found(client):

    response = client.get(
        "/opportunitys/999999"
    )

    assert response.status_code == 404
