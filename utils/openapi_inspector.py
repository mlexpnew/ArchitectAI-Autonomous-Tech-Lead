"""
ArchitectAI OpenAPI Inspector and Live API Tester

Provides utilities to extract OpenAPI specs from generated FastAPI applications,
generate sample request payloads, execute in-memory test requests via TestClient,
and render an embedded Swagger UI.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def extract_openapi_spec(backend_dir: Path) -> Optional[Dict[str, Any]]:
    """
    Extract the OpenAPI specification dictionary from a generated backend.
    Checks for an existing openapi.json first, and falls back to dynamic extraction.
    """
    openapi_file = backend_dir / "openapi.json"
    if openapi_file.exists():
        try:
            return json.loads(openapi_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    main_file = backend_dir / "app" / "main.py"
    if not main_file.exists():
        return None

    backend_path = str(backend_dir.resolve())
    script = f"""
import sys, json
sys.path.insert(0, {repr(backend_path)})
try:
    from app.main import app
    print("ARCHITECTAI_SPEC_START")
    print(json.dumps(app.openapi()))
    print("ARCHITECTAI_SPEC_END")
except Exception as e:
    import sys
    sys.exit(1)
"""
    try:
        res = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if res.returncode == 0 and "ARCHITECTAI_SPEC_START" in res.stdout:
            raw = res.stdout.split("ARCHITECTAI_SPEC_START")[1].split("ARCHITECTAI_SPEC_END")[0].strip()
            spec = json.loads(raw)
            # Cache to openapi.json
            try:
                openapi_file.write_text(json.dumps(spec, indent=2), encoding="utf-8")
            except Exception:
                pass
            return spec
    except Exception:
        pass

    return None


def resolve_schema_ref(ref_str: str, all_schemas: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve a '#/components/schemas/Name' reference."""
    if ref_str.startswith("#/components/schemas/"):
        name = ref_str.split("/")[-1]
        return all_schemas.get(name, {})
    return {}


def build_sample_payload(
    schema: Dict[str, Any],
    all_schemas: Dict[str, Any],
    depth: int = 0,
) -> Any:
    """
    Construct a clean, valid sample JSON payload for a given OpenAPI schema.
    """
    if depth > 3:
        return {}

    if "$ref" in schema:
        schema = resolve_schema_ref(schema["$ref"], all_schemas)

    prop_type = schema.get("type", "object")

    if prop_type == "object" or "properties" in schema:
        result = {}
        properties = schema.get("properties", {})
        for prop_name, prop_meta in properties.items():
            if prop_name.lower() == "id":
                continue

            if "$ref" in prop_meta:
                prop_meta = resolve_schema_ref(prop_meta["$ref"], all_schemas)

            p_type = prop_meta.get("type", "string")

            if p_type == "integer":
                result[prop_name] = 100
            elif p_type == "number":
                result[prop_name] = 49.99
            elif p_type == "boolean":
                result[prop_name] = True
            elif p_type == "array":
                item_schema = prop_meta.get("items", {})
                result[prop_name] = [build_sample_payload(item_schema, all_schemas, depth + 1)] if item_schema else []
            elif p_type == "object":
                result[prop_name] = build_sample_payload(prop_meta, all_schemas, depth + 1)
            else:
                # String format hints
                fmt = prop_meta.get("format", "")
                if fmt == "date":
                    result[prop_name] = "2026-09-30"
                elif fmt == "date-time":
                    result[prop_name] = "2026-09-30T10:00:00Z"
                elif fmt == "email":
                    result[prop_name] = "user@example.com"
                elif any(k in prop_name.lower() for k in ("name", "title", "label", "heading")):
                    result[prop_name] = f"Sample {prop_name.replace('_', ' ').title()}"
                elif "status" in prop_name.lower():
                    result[prop_name] = "ACTIVE"
                else:
                    result[prop_name] = f"sample_{prop_name}"
        return result

    elif prop_type == "array":
        item_schema = schema.get("items", {})
        return [build_sample_payload(item_schema, all_schemas, depth + 1)] if item_schema else []
    elif prop_type == "integer":
        return 1
    elif prop_type == "number":
        return 1.0
    elif prop_type == "boolean":
        return True
    else:
        return "sample_value"


def execute_test_request(
    backend_dir: Path,
    method: str,
    path: str,
    json_body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout_sec: int = 10,
) -> Dict[str, Any]:
    """
    Execute a real HTTP request against the generated FastAPI app using TestClient
    in an isolated subprocess, returning status_code, body, headers, and latency_ms.
    """
    backend_path = str(backend_dir.resolve())
    payload_repr = json.dumps(json_body) if json_body is not None else "None"
    params_repr = json.dumps(params) if params is not None else "None"

    script = f"""
import sys, json, time
sys.path.insert(0, {repr(backend_path)})
try:
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    t0 = time.perf_counter()

    body_arg = {payload_repr}
    params_arg = {params_repr}

    kwargs = {{}}
    if body_arg is not None:
        kwargs["json"] = body_arg
    if params_arg is not None:
        kwargs["params"] = params_arg

    response = client.request({repr(method.upper())}, {repr(path)}, **kwargs)
    latency_ms = (time.perf_counter() - t0) * 1000

    try:
        resp_body = response.json()
    except Exception:
        resp_body = response.text

    result = {{
        "status_code": response.status_code,
        "body": resp_body,
        "headers": dict(response.headers),
        "latency_ms": round(latency_ms, 2),
        "error": None
    }}
    print("ARCHITECTAI_REQ_START")
    print(json.dumps(result))
    print("ARCHITECTAI_REQ_END")
except Exception as e:
    err_result = {{
        "status_code": 500,
        "body": str(e),
        "headers": {{}},
        "latency_ms": 0.0,
        "error": str(e)
    }}
    print("ARCHITECTAI_REQ_START")
    print(json.dumps(err_result))
    print("ARCHITECTAI_REQ_END")
"""

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{backend_path}{os.pathsep}{env.get('PYTHONPATH', '')}"

    try:
        t_start = time.perf_counter()
        res = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=backend_dir,
            env=env,
        )
        total_time_ms = round((time.perf_counter() - t_start) * 1000, 2)

        if "ARCHITECTAI_REQ_START" in res.stdout:
            raw = res.stdout.split("ARCHITECTAI_REQ_START")[1].split("ARCHITECTAI_REQ_END")[0].strip()
            data = json.loads(raw)
            if data.get("latency_ms") == 0.0:
                data["latency_ms"] = total_time_ms
            return data

        return {
            "status_code": 500,
            "body": res.stderr.strip() or res.stdout.strip() or "Unknown execution error",
            "headers": {},
            "latency_ms": total_time_ms,
            "error": "Failed to parse TestClient response",
        }

    except subprocess.TimeoutExpired:
        return {
            "status_code": 504,
            "body": f"Request timed out after {timeout_sec}s",
            "headers": {},
            "latency_ms": float(timeout_sec * 1000),
            "error": "TimeoutExpired",
        }
    except Exception as exc:
        return {
            "status_code": 500,
            "body": str(exc),
            "headers": {},
            "latency_ms": 0.0,
            "error": str(exc),
        }


def render_swagger_ui_html(spec_dict: Dict[str, Any]) -> str:
    """
    Generate an HTML document that embeds Swagger UI with a modern dark theme.
    """
    spec_json = json.dumps(spec_dict)

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
  <style>
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      padding: 12px;
      background: #0d1117;
      color: #e6edf3;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .swagger-ui .topbar {{
      display: none;
    }}
    .swagger-ui {{
      color: #c9d1d9;
    }}
    .swagger-ui .info .title {{
      color: #f0f6fc;
      font-size: 22px;
      font-weight: 600;
    }}
    .swagger-ui .info p, .swagger-ui .info li {{
      color: #8b949e;
      font-size: 13px;
    }}
    .swagger-ui .scheme-container {{
      background: #161b22;
      box-shadow: none;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 10px 14px;
      margin-bottom: 16px;
    }}
    .swagger-ui .opblock {{
      background: #161b22;
      border-radius: 8px;
      border: 1px solid #30363d;
      box-shadow: none;
      margin-bottom: 10px;
    }}
    .swagger-ui .opblock .opblock-summary {{
      border-color: #30363d;
      padding: 8px 12px;
    }}
    .swagger-ui .opblock .opblock-summary-method {{
      border-radius: 6px;
      font-weight: 700;
      font-size: 12px;
      min-width: 70px;
    }}
    .swagger-ui .opblock .opblock-summary-path {{
      color: #f0f6fc;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 13px;
    }}
    .swagger-ui .opblock .opblock-summary-description {{
      color: #8b949e;
      font-size: 12px;
    }}
    .swagger-ui .opblock-body {{
      background: #0d1117;
      border-top: 1px solid #30363d;
      padding: 14px;
    }}
    .swagger-ui table thead tr td, .swagger-ui table thead tr th {{
      color: #8b949e;
      border-color: #30363d;
      font-size: 12px;
    }}
    .swagger-ui .tab li button.tablinks {{
      color: #8b949e;
    }}
    .swagger-ui .tab li button.tablinks.active {{
      color: #58a6ff;
    }}
    .swagger-ui section.models {{
      border: 1px solid #30363d;
      border-radius: 8px;
      background: #161b22;
    }}
    .swagger-ui section.models h4 {{
      color: #f0f6fc;
      font-size: 14px;
    }}
    .swagger-ui .model-box {{
      background: #0d1117;
      border-radius: 6px;
    }}
    .swagger-ui .model {{
      color: #c9d1d9;
    }}
    .swagger-ui .prop-type {{
      color: #58a6ff;
    }}
    .swagger-ui select {{
      background: #161b22;
      color: #f0f6fc;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 4px 8px;
    }}
    .swagger-ui input[type=text] {{
      background: #0d1117;
      color: #f0f6fc;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 6px 10px;
    }}
    .swagger-ui textarea {{
      background: #0d1117;
      color: #f0f6fc;
      border: 1px solid #30363d;
      border-radius: 6px;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    }}
    .swagger-ui .btn {{
      border-radius: 6px;
      font-size: 12px;
      font-weight: 500;
    }}
    .swagger-ui .btn.execute {{
      background-color: #238636;
      color: #ffffff;
      border-color: #2ea043;
    }}
    .swagger-ui .btn.btn-clear {{
      background: #21262d;
      color: #c9d1d9;
      border-color: #30363d;
    }}
    .swagger-ui .responses-inner h4, .swagger-ui .responses-inner h5 {{
      color: #f0f6fc;
    }}
    .swagger-ui .response-col_status {{
      color: #58a6ff;
    }}
    .swagger-ui .highlight-code pre {{
      background: #0d1117 !important;
      border: 1px solid #30363d;
      border-radius: 6px;
      color: #e6edf3;
    }}
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {{
      const spec = {spec_json};
      window.ui = SwaggerUIBundle({{
        spec: spec,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      }});
    }};
  </script>
</body>
</html>
"""
