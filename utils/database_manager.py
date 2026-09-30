"""
ArchitectAI Database & Migration Manager

Provides helper utilities to apply Alembic migrations and run the
synthetic mock data seeder against generated FastAPI backend projects.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict


def apply_migrations(backend_dir: Path, timeout_sec: int = 15) -> Dict[str, Any]:
    """
    Run 'alembic upgrade head' in the generated project.
    """
    backend_path = str(backend_dir.resolve())
    alembic_ini = backend_dir / "alembic.ini"

    if not alembic_ini.exists():
        return {
            "success": False,
            "stdout": "",
            "stderr": "alembic.ini not found in backend directory",
            "returncode": 1,
        }

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{backend_path}{os.pathsep}{env.get('PYTHONPATH', '')}"

    try:
        t0 = time.perf_counter()
        res = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=backend_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

        return {
            "success": res.returncode == 0,
            "stdout": res.stdout.strip(),
            "stderr": res.stderr.strip(),
            "returncode": res.returncode,
            "latency_ms": elapsed_ms,
        }
    except Exception as exc:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(exc),
            "returncode": -1,
            "latency_ms": 0.0,
        }


def seed_database(backend_dir: Path, timeout_sec: int = 15) -> Dict[str, Any]:
    """
    Execute 'python seed.py' in the generated project to populate synthetic demo data.
    """
    backend_path = str(backend_dir.resolve())
    seed_script = backend_dir / "seed.py"

    if not seed_script.exists():
        return {
            "success": False,
            "stdout": "",
            "stderr": "seed.py not found in backend directory",
            "returncode": 1,
            "summary": {},
        }

    script = f"""
import sys, json, os
sys.path.insert(0, {repr(backend_path)})
try:
    from seed import seed
    summary = seed()
    print("ARCHITECTAI_SEED_START")
    print(json.dumps(summary or {{}}))
    print("ARCHITECTAI_SEED_END")
except Exception as e:
    import sys
    print("ARCHITECTAI_SEED_ERR: " + str(e), file=sys.stderr)
    sys.exit(1)
"""

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{backend_path}{os.pathsep}{env.get('PYTHONPATH', '')}"

    try:
        t0 = time.perf_counter()
        res = subprocess.run(
            [sys.executable, "-c", script],
            cwd=backend_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

        summary = {}
        if "ARCHITECTAI_SEED_START" in res.stdout:
            raw = res.stdout.split("ARCHITECTAI_SEED_START")[1].split("ARCHITECTAI_SEED_END")[0].strip()
            try:
                summary = json.loads(raw)
            except Exception:
                pass

        return {
            "success": res.returncode == 0,
            "stdout": res.stdout.strip(),
            "stderr": res.stderr.strip(),
            "returncode": res.returncode,
            "summary": summary,
            "latency_ms": elapsed_ms,
        }
    except Exception as exc:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(exc),
            "returncode": -1,
            "summary": {},
            "latency_ms": 0.0,
        }
