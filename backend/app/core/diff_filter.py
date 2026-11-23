from pathlib import PurePosixPath
from typing import Any

LOCKFILE_NAMES: frozenset[str] = frozenset(
    {
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "uv.lock",
        "poetry.lock",
        "cargo.lock",
        "composer.lock",
    }
)

IGNORED_DIR_SEGMENTS: frozenset[str] = frozenset(
    {
        "dist",
        "build",
        "node_modules",
        ".venv",
        "__pycache__",
        ".next",
        "coverage",
    }
)

IGNORED_SUFFIXES: tuple[str, ...] = (".min.js", ".min.css", ".map")


def is_ignored_path(path: str) -> bool:
    """Return True if path is a lockfile, minified/map asset, or inside an ignored build dir."""
    normalized = path.strip().replace("\\", "/").lstrip("/")
    if not normalized:
        return True

    posix = PurePosixPath(normalized)
    filename_lower = posix.name.lower()

    if filename_lower in LOCKFILE_NAMES:
        return True

    if filename_lower.endswith(IGNORED_SUFFIXES):
        return True

    for part in posix.parts[:-1]:
        if part.lower() in IGNORED_DIR_SEGMENTS:
            return True

    return False


def filter_changed_files(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filter a list of GitHub commit/PR file dicts, keeping only non-ignored source files."""
    kept: list[dict[str, Any]] = []
    for file_item in files:
        filename = str(file_item.get("filename") or file_item.get("path") or "")
        if not filename or is_ignored_path(filename):
            continue
        kept.append(file_item)
    return kept
