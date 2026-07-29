"""
Employee API Smoke Tests
"""


def test_employee_get_all(client):

    response = client.get(
        "/employees/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_employee_not_found(client):

    response = client.get(
        "/employees/999999"
    )

    assert response.status_code == 404
