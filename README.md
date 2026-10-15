# Development Orchestrator

A project-agnostic control plane for coordinating software delivery across repositories and issue trackers.

## Current MVP

- Responsive project dashboard.
- SQLite-backed project registry with JSON API.
- Read-only GitHub repository metadata snapshots.
- Read-only Jira project metadata snapshots.
- Environment-based integration credentials.
- Initial pytest suite and GitHub Actions workflow.

## Local setup

1. Install Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and set a strong `FLASK_SECRET_KEY`.
5. Run `python app.py` and open `http://localhost:5000`.
6. Run tests with `pytest -q`.

Configure `GITHUB_TOKEN` only if needed for private repositories. Configure `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN` to enable Jira snapshots. Keep credentials in environment variables or a secrets manager; never commit them.

## API

- `GET /api/health` — health check.
- `GET /api/projects` — list registered projects.
- `POST /api/projects` — create a project with JSON fields `name`, `repository_url`, and optional `jira_project_key`.
- `DELETE /api/projects/<id>` — remove a project.

## Approval and security policy

This milestone reads provider metadata only. It does not execute code changes, create pull requests, merge changes, or deploy releases. Future merge and production-release operations must require explicit human approval and authoritative verification checks.

This MVP is not production-ready. Before exposing it publicly, implement authentication, authorization, CSRF protection, database migrations, audit logging, and deployment-specific secret management. Use least-privilege provider tokens.

See `docs/architecture.md` for the staged roadmap.
