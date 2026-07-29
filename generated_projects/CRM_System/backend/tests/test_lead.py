"""
Lead API Smoke Tests
"""


def test_lead_get_all(client):

    response = client.get(
        "/leads/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_lead_not_found(client):

    response = client.get(
        "/leads/999999"
    )

    assert response.status_code == 404
