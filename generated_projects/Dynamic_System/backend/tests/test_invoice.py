"""
Invoice API Smoke Tests
"""


def test_invoice_get_all(client):

    response = client.get(
        "/invoices/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_invoice_not_found(client):

    response = client.get(
        "/invoices/999999"
    )

    assert response.status_code == 404
