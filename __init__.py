"""hosting-digest plugin — manually trigger hosting cost digest reports.

Registers ``/hosting-digest`` as a Hermes gateway/CLI slash command. The command
runs the same script used by the scheduled Vultr cost digest so operators can
request an on-demand infrastructure cost snapshot without waiting for cron.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_TIMEOUT_SECONDS = 60


def _hermes_home() -> Path:
    configured = os.getenv("HERMES_HOME", "").strip()
    return Path(configured).expanduser() if configured else Path.home() / ".hermes"


def _default_script_path() -> Path:
    return _hermes_home() / "scripts" / "vultr_cost_digest.py"


def _script_path() -> Path:
    configured = os.getenv("HOSTING_DIGEST_SCRIPT", "").strip()
    return Path(configured).expanduser() if configured else _default_script_path()


def _handle_slash(raw_args: str) -> str:
    argv = raw_args.strip().split()
    if argv and argv[0] in {"help", "-h", "--help"}:
        return (
            "/hosting-digest — run the hosting cost digest now\n\n"
            "This runs the same digest script used by the scheduled hosting cost cron.\n"
            "Set HOSTING_DIGEST_SCRIPT to override the default script path."
        )

    script = _script_path()
    if not script.exists():
        return f"hosting-digest script not found: {script}"

    env = os.environ.copy()
    env.setdefault("HERMES_HOME", str(_hermes_home()))

    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            text=True,
            capture_output=True,
            timeout=DEFAULT_TIMEOUT_SECONDS,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"hosting-digest timed out after {DEFAULT_TIMEOUT_SECONDS}s."
    except Exception as exc:  # pragma: no cover - defensive fallback
        return f"hosting-digest failed to start: {exc}"

    output = (proc.stdout or proc.stderr or "").strip()
    if proc.returncode != 0:
        detail = output or f"exit code {proc.returncode}"
        return f"hosting-digest failed: {detail}"
    return output or "hosting-digest completed with no output."


def register(ctx) -> None:
    ctx.register_command(
        "hosting-digest",
        handler=_handle_slash,
        description="Run the hosting infrastructure cost digest now.",
    )
