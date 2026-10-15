import os
from urllib.parse import urlparse
import requests

TIMEOUT_SECONDS = 8

def github_snapshot(repository_url):
    token = os.getenv("GITHUB_TOKEN", "").strip()
    parsed = urlparse((repository_url or "").strip())
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if parsed.netloc.lower() != "github.com" or len(parts) < 2:
        return {"status": "not_configured", "message": "Use a GitHub repository URL."}
    owner, repo = parts[0], parts[1].removesuffix(".git")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers, timeout=TIMEOUT_SECONDS)
        if response.status_code == 404:
            return {"status": "unavailable", "message": "Repository not found or not accessible."}
        response.raise_for_status()
        data = response.json()
        return {"status": "connected", "default_branch": data.get("default_branch", ""), "open_issues": data.get("open_issues_count", 0), "updated_at": data.get("updated_at", ""), "html_url": data.get("html_url", repository_url)}
    except (requests.RequestException, ValueError):
        return {"status": "error", "message": "GitHub status could not be retrieved."}

def jira_snapshot(project_key):
    base_url = os.getenv("JIRA_BASE_URL", "").strip().rstrip("/")
    email = os.getenv("JIRA_EMAIL", "").strip()
    token = os.getenv("JIRA_API_TOKEN", "").strip()
    if not base_url or not email or not token or not project_key:
        return {"status": "not_configured", "message": "Configure Jira credentials and a project key."}
    try:
        response = requests.get(f"{base_url}/rest/api/3/project/{project_key}", auth=(email, token), headers={"Accept": "application/json"}, timeout=TIMEOUT_SECONDS)
        if response.status_code == 404:
            return {"status": "unavailable", "message": "Jira project not found or not accessible."}
        response.raise_for_status()
        data = response.json()
        return {"status": "connected", "name": data.get("name", project_key), "key": data.get("key", project_key), "url": f"{base_url}/browse/{project_key}"}
    except (requests.RequestException, ValueError):
        return {"status": "error", "message": "Jira status could not be retrieved."}
