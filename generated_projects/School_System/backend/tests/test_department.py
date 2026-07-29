"""
Department API Smoke Tests
"""


def test_department_get_all(client):

    response = client.get(
        "/departments/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_department_not_found(client):

    response = client.get(
        "/departments/999999"
    )

    assert response.status_code == 404
