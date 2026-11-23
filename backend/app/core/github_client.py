import os
from typing import Any
from urllib.parse import urlparse

import httpx

GITHUB_API_BASE = "https://api.github.com"
MAX_COMMITS = 100
MAX_DETAILED_COMMITS = 15
MAX_PRS = 30


class RepoNotFoundError(Exception):
    """Raised when the target GitHub repository does not exist or is private (HTTP 404)."""


class GitHubRateLimitError(Exception):
    """Raised when GitHub API rate limit is exceeded (HTTP 403/429)."""


class GitHubUpstreamError(Exception):
    """Raised when GitHub API returns an unexpected error or network failure."""


def parse_github_repo_url(repo_url: str) -> tuple[str, str]:
    """Parse and validate a GitHub repository URL into (owner, repo).

    Raises ValueError if the URL is not a valid https://github.com/<owner>/<repo> URL.
    """
    raw = (repo_url or "").strip()
    if not raw:
        raise ValueError("Repository URL must not be empty.")

    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Repository URL must use http or https scheme.")

    host = (parsed.hostname or "").lower()
    if host not in {"github.com", "www.github.com"}:
        raise ValueError("Repository URL must point to github.com.")

    segments = [seg for seg in parsed.path.strip("/").split("/") if seg]
    if len(segments) < 2:
        raise ValueError("Repository URL must include both owner and repository name.")

    owner, repo = segments[0].strip(), segments[1].strip()
    if repo.endswith(".git"):
        repo = repo[:-4]

    if not owner or not repo:
        raise ValueError("Invalid owner or repository name in GitHub URL.")

    return owner, repo


def _check_response_errors(response: httpx.Response, owner: str, repo: str) -> None:
    status = response.status_code
    if status == 404:
        raise RepoNotFoundError(f"GitHub repository '{owner}/{repo}' not found (404).")

    if status == 429:
        raise GitHubRateLimitError("GitHub API rate limit exceeded (429).")

    if status == 403:
        remaining = response.headers.get("x-ratelimit-remaining", "")
        body_lower = response.text.lower()
        if remaining == "0" or "rate limit" in body_lower:
            raise GitHubRateLimitError("GitHub API rate limit exceeded (403).")
        raise GitHubUpstreamError(f"GitHub API access forbidden (403) for '{owner}/{repo}'.")

    if status >= 400:
        raise GitHubUpstreamError(
            f"GitHub API returned unexpected HTTP {status} for '{owner}/{repo}'."
        )


def fetch_repo_telemetry(
    owner: str,
    repo: str,
    token: str | None = None,
) -> dict[str, Any]:
    """Fetch bounded commits, recent file changes, and PRs from GitHub REST API."""
    resolved_token = token if token is not None else os.getenv("GITHUB_TOKEN", "").strip()
    headers: dict[str, str] = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "vku-sprintguard-backend/0.1.0",
    }
    if resolved_token:
        headers["Authorization"] = f"Bearer {resolved_token}"

    try:
        with httpx.Client(
            base_url=GITHUB_API_BASE,
            headers=headers,
            timeout=15.0,
            follow_redirects=True,
        ) as client:
            commits_resp = client.get(
                f"/repos/{owner}/{repo}/commits",
                params={"per_page": MAX_COMMITS},
            )
            _check_response_errors(commits_resp, owner, repo)
            raw_commits = commits_resp.json()
            if not isinstance(raw_commits, list):
                raw_commits = []

            commits: list[dict[str, Any]] = []
            for idx, item in enumerate(raw_commits[:MAX_COMMITS]):
                if not isinstance(item, dict):
                    continue
                sha = str(item.get("sha") or "")
                commit_obj = item.get("commit") or {}
                author_obj = item.get("author") or {}
                commit_author = commit_obj.get("author") or {}

                login = str(author_obj.get("login") or commit_author.get("name") or "unknown")
                author_name = str(commit_author.get("name") or login)
                date_str = str(commit_author.get("date") or "")

                files: list[dict[str, Any]] = item.get("files") or []
                if not files and sha and idx < MAX_DETAILED_COMMITS:
                    try:
                        detail_resp = client.get(f"/repos/{owner}/{repo}/commits/{sha}")
                        if detail_resp.status_code == 200:
                            detail_data = detail_resp.json()
                            if isinstance(detail_data, dict):
                                files = detail_data.get("files") or []
                    except httpx.HTTPError:
                        # Gracefully degrade if a single commit detail call times out
                        files = []

                commits.append(
                    {
                        "sha": sha,
                        "author_login": login,
                        "author_name": author_name,
                        "date": date_str,
                        "message": str(commit_obj.get("message") or ""),
                        "files": files,
                    }
                )

            prs: list[dict[str, Any]] = []
            try:
                prs_resp = client.get(
                    f"/repos/{owner}/{repo}/pulls",
                    params={"state": "all", "per_page": MAX_PRS},
                )
                if prs_resp.status_code == 200 and isinstance(prs_resp.json(), list):
                    for pr in prs_resp.json()[:MAX_PRS]:
                        if isinstance(pr, dict):
                            prs.append(
                                {
                                    "number": pr.get("number"),
                                    "title": pr.get("title"),
                                    "state": pr.get("state"),
                                    "user_login": (pr.get("user") or {}).get("login"),
                                    "created_at": pr.get("created_at"),
                                }
                            )
            except httpx.HTTPError:
                prs = []

            return {"commits": commits, "prs": prs}
    except (RepoNotFoundError, GitHubRateLimitError, GitHubUpstreamError):
        raise
    except httpx.HTTPError as exc:
        raise GitHubUpstreamError(f"Network error communicating with GitHub API: {exc}") from exc
