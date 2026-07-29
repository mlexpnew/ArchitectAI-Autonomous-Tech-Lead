"""
Loan API Smoke Tests
"""


def test_loan_get_all(client):

    response = client.get(
        "/loans/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_loan_not_found(client):

    response = client.get(
        "/loans/999999"
    )

    assert response.status_code == 404
