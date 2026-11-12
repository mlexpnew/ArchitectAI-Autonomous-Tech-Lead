"""Does the code ArchitectAI writes actually work? Measured, not claimed.

    MOCK_LLM=true python benchmark/verify_generated.py --out benchmark/results

For each specification in examples/:
  1. generate     the generator finishes (and how long it takes)
  2. compiles     every generated .py file compiles
  3. boots        the FastAPI app imports and serves /openapi.json
  4. CRUD         every entity survives create -> read -> compare -> update -> delete -> 404
  5. own tests    the project's generated pytest suite passes

Mock LLM mode makes the run free and reproducible; set a provider key and drop
MOCK_LLM to measure a real model instead.
"""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMOKE = Path(__file__).resolve().parent / "smoke_api.py"


def specs() -> list[tuple[str, Path]]:
    out = []
    for f in sorted((ROOT / "examples").glob("*_requirements.txt")):
        name = f.stem.replace("_requirements", "").replace("_", " ").title() + " Management System"
        out.append((name, f))
    return out


def compile_all(folder: Path) -> tuple[int, int, list[str]]:
    files = list(folder.rglob("*.py"))
    bad = []
    for f in files:
        try:
            py_compile.compile(str(f), doraise=True)
        except py_compile.PyCompileError as exc:
            bad.append(f"{f.relative_to(folder)}: {str(exc).splitlines()[-1][:120]}")
    return len(files) - len(bad), len(files), bad


def find_backend(out: Path) -> Path | None:
    hits = sorted(out.rglob("app/main.py"), key=lambda p: len(p.parts))
    return hits[0].parent.parent if hits else None


def pytest_counts(backend: Path, timeout: int) -> dict:
    if not (backend / "tests").exists():
        return {"passed": 0, "total": 0}
    env = dict(os.environ, DATABASE_URL="sqlite:///./pytest_bench.db", PYTHONPATH=str(backend))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests"],
                       cwd=backend, capture_output=True, text=True, timeout=timeout, env=env)  # fmt: skip
    tail = (r.stdout + r.stderr)[-2000:]
    passed = sum(int(n) for n in re.findall(r"(\d+) passed", tail))
    failed = sum(int(n) for n in re.findall(r"(\d+) (?:failed|error)", tail))
    return {"passed": passed, "total": passed + failed}


def run_one(name: str, spec: Path, workdir: Path, timeout: int) -> dict:
    out = workdir / spec.stem
    row: dict = {"project": name, "generated": False, "seconds": None}
    t0 = time.perf_counter()
    try:
        g = subprocess.run([sys.executable, "architectai.py", "generate", "--name", name,
                            "--requirements", str(spec), "--output", str(out)],
                           cwd=ROOT, capture_output=True, text=True, timeout=timeout)  # fmt: skip
        row["seconds"] = round(time.perf_counter() - t0, 1)
        row["generated"] = g.returncode == 0
        if g.returncode != 0:
            row["error"] = (g.stderr or g.stdout)[-300:]
    except subprocess.TimeoutExpired:
        row["error"] = f"generation timed out after {timeout}s"
    backend = find_backend(out) if out.exists() else None
    if backend is None:
        row["error"] = row.get("error") or "no app/main.py generated"
        return row
    ok, total, bad = compile_all(backend)
    row["compiles"] = {"passed": ok, "total": total}
    if bad:
        row["compile_errors"] = bad[:5]
    try:
        s = subprocess.run([sys.executable, str(SMOKE)], cwd=backend, capture_output=True,
                           text=True, timeout=timeout,
                           env=dict(os.environ, DATABASE_URL="sqlite:///./smoke_test.db"))  # fmt: skip
        smoke = json.loads(s.stdout.strip().splitlines()[-1]) if s.stdout.strip() else {}
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        smoke = {"imports": False, "failures": [f"smoke runner: {exc}"[:200]]}
    row["boots"] = smoke.get("imports", False)
    row["entities"] = smoke.get("entities", 0)
    row["crud"] = smoke.get("stages", {})
    row["crud_failures"] = smoke.get("failures", [])[:6]
    try:
        row["own_tests"] = pytest_counts(backend, timeout)
    except subprocess.TimeoutExpired:
        row["own_tests"] = {"passed": 0, "total": 0, "error": "timeout"}
    return row


def crud_rate(row: dict) -> tuple[int, int]:
    stages = row.get("crud") or {}
    return (sum(v["passed"] for v in stages.values()), sum(v["total"] for v in stages.values()))


def report(rows: list[dict], mode: str) -> str:
    def pct(a, b):
        return f"{a}/{b} ({a / b:.0%})" if b else "n/a"

    lines = [
        f"### ArchitectAI verification ({len(rows)} specifications, LLM mode: {mode})",
        "",
        "| Project | Generated | .py files compile | App boots | Entities | CRUD checks passed "
        "| Its own tests pass | Time (s) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        c = r.get("compiles", {"passed": 0, "total": 0})
        t = r.get("own_tests", {"passed": 0, "total": 0})
        lines.append(
            f"| {r['project']} | {'yes' if r['generated'] else 'no'} | "
            f"{pct(c['passed'], c['total'])} | {'yes' if r.get('boots') else 'no'} | "
            f"{r.get('entities', 0)} | {pct(*crud_rate(r))} | {pct(t['passed'], t['total'])} | "
            f"{r.get('seconds') or '-'} |"
        )
    gen = sum(r["generated"] for r in rows)
    boots = sum(bool(r.get("boots")) for r in rows)
    cp, ct = (sum(crud_rate(r)[i] for r in rows) for i in (0, 1))
    fully = sum(bool(r.get("boots")) and crud_rate(r)[1] > 0 and crud_rate(r)[0] == crud_rate(r)[1]
                for r in rows)  # fmt: skip
    lines += [
        "",
        "| Summary | Result |",
        "|---|---|",
        f"| Projects generated | {pct(gen, len(rows))} |",
        f"| Projects whose app boots | {pct(boots, len(rows))} |",
        f"| Projects passing every CRUD check | {pct(fully, len(rows))} |",
        f"| CRUD checks passed overall | {pct(cp, ct)} |",
    ]
    fails = [f"- **{r['project']}**: " + "; ".join((r.get("crud_failures") or
             [r.get("error", "")])[:3]) for r in rows if r.get("crud_failures") or r.get("error")]  # fmt: skip
    if fails:
        lines += ["", "**First failures per project** (what to fix next):", "", *fails]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--out", default="benchmark/results")
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--only", default="", help="comma-separated spec names, e.g. library,crm")
    a = p.parse_args(argv)
    chosen = specs()
    if a.only:
        keep = {s.strip().lower() for s in a.only.split(",")}
        chosen = [s for s in chosen if s[1].stem.split("_")[0] in keep]
    mode = "mock" if os.getenv("MOCK_LLM", "").lower() in ("1", "true", "yes") else "live"
    work = Path(tempfile.mkdtemp(prefix="architectai_bench_"))
    rows = []
    try:
        for name, spec in chosen:
            print(f"== {name}", file=sys.stderr, flush=True)
            rows.append(run_one(name, spec, work, a.timeout))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(rows, indent=2))
    md = report(rows, mode)
    (out / "report.md").write_text(md)
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
