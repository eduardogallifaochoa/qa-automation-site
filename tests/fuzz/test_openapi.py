# tests/fuzz/test_openapi.py
import os
import sys
import shutil
import subprocess

OPENAPI_URL = os.getenv("OPENAPI_URL", "http://127.0.0.1:8000/openapi.json")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
MAX_EXAMPLES = int(os.getenv("FUZZ_EXAMPLES", "10"))

def _child_env() -> dict:
    """Force UTF-8 & no color so Windows consoles don't choke on Unicode output."""
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("NO_COLOR", "1")  # click respects NO_COLOR; keeps output plain
    return env

def test_schemathesis_cli():
    # Prefer the console script; fall back to module execution if needed.
    exe = shutil.which("schemathesis") or shutil.which("st")
    if exe:
        cmd = [
            exe, "run",
            OPENAPI_URL,
            "--url", BASE_URL,          # Schemathesis 4.x uses --url
            "--checks", "all",
            "--max-examples", str(MAX_EXAMPLES),
        ]
    else:
        cmd = [
            sys.executable, "-m", "schemathesis.cli",
            "run",
            OPENAPI_URL,
            "--url", BASE_URL,
            "--checks", "all",
            "--max-examples", str(MAX_EXAMPLES),
        ]

    # Explicitly decode as UTF-8 to avoid UnicodeDecodeError in the reader thread on Windows.
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=_child_env(),
    )
    # Print outputs to help debugging in CI logs (now safely decoded).
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    assert result.returncode == 0, f"Schemathesis CLI run failed (exit {result.returncode})"
