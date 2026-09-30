"""
Tests for utils/openapi_inspector.py
"""

import tempfile
from pathlib import Path

from utils.openapi_inspector import (
    extract_openapi_spec,
    build_sample_payload,
    execute_test_request,
    render_swagger_ui_html,
)


def test_build_sample_payload_primitives():
    all_schemas = {}
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "price": {"type": "number"},
            "in_stock": {"type": "boolean"},
            "created_date": {"type": "string", "format": "date"},
            "contact_email": {"type": "string", "format": "email"},
            "item_status": {"type": "string"},
        }
    }
    payload = build_sample_payload(schema, all_schemas)
    assert "id" not in payload  # id should be skipped
    assert payload["title"] == "Sample Title"
    assert payload["price"] == 49.99
    assert payload["in_stock"] is True
    assert payload["created_date"] == "2026-09-30"
    assert payload["contact_email"] == "user@example.com"
    assert payload["item_status"] == "ACTIVE"


def test_build_sample_payload_with_ref():
    all_schemas = {
        "Address": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "zip_code": {"type": "integer"},
            }
        }
    }
    schema = {
        "$ref": "#/components/schemas/Address"
    }
    payload = build_sample_payload(schema, all_schemas)
    assert payload["city"] == "sample_city"
    assert payload["zip_code"] == 100


def test_render_swagger_ui_html():
    spec = {
        "openapi": "3.1.0",
        "info": {"title": "Test Service", "version": "1.0.0"},
        "paths": {"/": {"get": {"summary": "Root"}}}
    }
    html = render_swagger_ui_html(spec)
    assert "<!DOCTYPE html>" in html
    assert "swagger-ui" in html
    assert "Test Service" in html


def test_extract_openapi_spec_on_existing_backend():
    backend_dir = Path("outputs/Hospital_Management_System/backend")
    if backend_dir.exists():
        spec = extract_openapi_spec(backend_dir)
        assert spec is not None
        assert "openapi" in spec
        assert "paths" in spec
        assert "/" in spec["paths"] or len(spec["paths"]) > 0


def test_execute_test_request_on_existing_backend():
    backend_dir = Path("outputs/Hospital_Management_System/backend")
    if backend_dir.exists():
        res = execute_test_request(backend_dir, "GET", "/")
        assert res["status_code"] == 200
        assert res["body"]["status"] == "running"
        assert res["latency_ms"] >= 0.0


def test_extract_openapi_spec_missing_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        res = extract_openapi_spec(Path(tmpdir))
        assert res is None
