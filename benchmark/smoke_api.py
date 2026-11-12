"""CRUD round-trip against a generated backend. Run from inside that backend folder.

    python smoke_api.py > result.json

For every collection endpoint in the OpenAPI spec: create a record from the request
schema, read it back and compare fields, update it, delete it, and confirm it is gone.
Parent entities are created first so foreign keys (`author_id`, ...) point at real rows.
Prints one JSON object; never raises, so one broken project cannot hide the others.
"""

from __future__ import annotations

import json
import os
import re
import sys
import traceback

SAMPLE = {"string": "sample", "integer": 1, "number": 9.5, "boolean": True}
FORMATS = {"email": "user@example.com", "date": "2026-01-15", "date-time": "2026-01-15T10:00:00",
           "uuid": "123e4567-e89b-12d3-a456-426614174000", "uri": "https://example.com"}  # fmt: skip


def resolve(spec: dict, schema: dict) -> dict:
    while "$ref" in schema:
        name = schema["$ref"].split("/")[-1]
        schema = spec["components"]["schemas"][name]
    if "allOf" in schema:
        merged = {"properties": {}, "required": []}
        for part in schema["allOf"]:
            part = resolve(spec, part)
            merged["properties"].update(part.get("properties", {}))
            merged["required"] += part.get("required", [])
        return merged
    return schema


def value_for(spec: dict, prop: dict, name: str, n: int, ids: dict[str, int]):
    prop = resolve(spec, prop)
    if "anyOf" in prop:  # Optional[X] -> first non-null option
        prop = next((resolve(spec, p) for p in prop["anyOf"] if p.get("type") != "null"), {})
    if name.endswith("_id"):
        parent = name[:-3].replace("_", "")
        return ids.get(parent, 1)
    if "enum" in prop:
        return prop["enum"][0]
    t = prop.get("type", "string")
    if t == "string":
        if prop.get("format") in FORMATS:
            return FORMATS[prop["format"]]
        if "email" in name:
            return f"user{n}@example.com"
        return f"{name}-{n}"[: prop.get("maxLength", 60)]
    if t == "integer":
        return max(prop.get("minimum", 1), 1) + n
    if t == "number":
        return float(max(prop.get("minimum", 1), 1)) + 0.5
    if t == "array":
        return []
    return SAMPLE.get(t, f"{name}-{n}")


def payload(spec: dict, schema: dict, n: int, ids: dict[str, int]) -> dict:
    schema = resolve(spec, schema)
    return {k: value_for(spec, v, k, n, ids) for k, v in schema.get("properties", {}).items()}


def collections(spec: dict) -> list[tuple[str, dict]]:
    """(path, create schema) for every POST collection with a matching /{id} item path."""
    out = []
    for path, ops in spec.get("paths", {}).items():
        if "{" in path or "post" not in ops:
            continue
        body = ops["post"].get("requestBody", {}).get("content", {}).get("application/json")
        if not body:
            continue
        out.append((path, body["schema"]))
    return out


def order_by_dependencies(spec: dict, cols: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
    """Entities without foreign keys first, so children can reference real parents."""
    def fks(schema):
        return sum(k.endswith("_id") for k in resolve(spec, schema).get("properties", {}))
    return sorted(cols, key=lambda c: fks(c[1]))


def entity(path: str) -> str:
    seg = [s for s in path.strip("/").split("/") if s and not s.startswith("api") and s != "v1"]
    name = (seg[-1] if seg else path).replace("-", "").replace("_", "")
    for plural, single in (("ies", "y"), ("sses", "ss"), ("xes", "x"), ("ches", "ch"),
                           ("shes", "sh"), ("ses", "s")):  # fmt: skip
        if name.endswith(plural):
            return name[: -len(plural)] + single
    return name[:-1] if name.endswith("s") and not name.endswith("ss") else name


def main() -> dict:
    os.environ.setdefault("DATABASE_URL", "sqlite:///./smoke_test.db")
    sys.path.insert(0, os.getcwd())
    result = {"imports": False, "entities": 0, "stages": {}, "failures": []}
    try:
        from fastapi.testclient import TestClient

        from app.main import app
    except Exception as exc:
        result["failures"].append(f"import: {type(exc).__name__}: {exc}"[:300])
        return result
    result["imports"] = True
    stages = {k: [0, 0] for k in ("create", "read", "matches", "list", "update", "delete", "gone")}
    with TestClient(app) as c:
        spec = c.get("/openapi.json").json()
        cols = order_by_dependencies(spec, collections(spec))
        result["entities"] = len(cols)
        ids: dict[str, int] = {}
        for n, (path, schema) in enumerate(cols, 1):
            name = entity(path)
            base = path.rstrip("/")

            def check(stage, ok, why=""):
                stages[stage][1] += 1
                stages[stage][0] += bool(ok)
                if not ok:
                    result["failures"].append(f"{name}.{stage}: {why}"[:200])
                return ok

            body = payload(spec, schema, n, ids)
            r = c.post(path, json=body)
            if not check("create", r.status_code in (200, 201), f"{r.status_code} {r.text[:120]}"):
                continue
            created = r.json()
            item_id = created.get("id")
            if item_id is None:
                check("read", False, "create response has no id")
                continue
            ids[name] = item_id
            r = c.get(f"{base}/{item_id}")
            if check("read", r.status_code == 200, f"{r.status_code}"):
                got = r.json()
                diff = [k for k, v in body.items() if k in got and got[k] != v
                        and not (isinstance(v, str) and str(got[k]).startswith(v[:10]))]  # fmt: skip
                check("matches", not diff, f"fields differ: {diff}")
            r = c.get(path)
            check("list", r.status_code == 200 and isinstance(r.json(), list), f"{r.status_code}")
            upd = {k: v for k, v in payload(spec, schema, n + 100, ids).items()
                   if not k.endswith("_id")}  # fmt: skip
            r = c.put(f"{base}/{item_id}", json=upd)
            if r.status_code == 405:
                r = c.patch(f"{base}/{item_id}", json=upd)
            check("update", r.status_code == 200, f"{r.status_code} {r.text[:120]}")
        for path, _ in reversed(cols):  # children first, so deletes respect foreign keys
            name = entity(path)
            if name not in ids:
                continue
            base = path.rstrip("/")
            r = c.delete(f"{base}/{ids[name]}")
            stages["delete"][1] += 1
            stages["delete"][0] += r.status_code in (200, 202, 204)
            if r.status_code not in (200, 202, 204):
                result["failures"].append(f"{name}.delete: {r.status_code}")
            r = c.get(f"{base}/{ids[name]}")
            stages["gone"][1] += 1
            stages["gone"][0] += r.status_code == 404
    result["stages"] = {k: {"passed": v[0], "total": v[1]} for k, v in stages.items()}
    return result


if __name__ == "__main__":
    try:
        out = main()
    except Exception:
        out = {"imports": False, "failures": [traceback.format_exc()[-400:]], "stages": {}}
    print(json.dumps(out))
