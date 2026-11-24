"""VKU SprintGuard MCP Harness package."""

import sys
from pathlib import Path

_BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
if _BACKEND_DIR.is_dir() and str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from mcp_server.harness import (  # noqa: E402
    AuditSession,
    HarnessGuardError,
    SessionState,
    SprintGuardHarness,
)

__all__ = [
    "AuditSession",
    "HarnessGuardError",
    "SessionState",
    "SprintGuardHarness",
]
