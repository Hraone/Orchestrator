# Architecture and implementation roadmap

## Purpose

A project-agnostic control plane for coordinating delivery workflows across multiple software repositories and issue trackers. The orchestrator owns project metadata, workflow state, approvals, and audit events; it does not replace each project's source repository or issue tracker.

## Current MVP

- Flask web dashboard and JSON API.
- SQLite-backed project registry.
- Read-only GitHub repository metadata snapshots.
- Read-only Jira project metadata snapshots.
- Environment-based credentials; no tokens stored in the database.
- Responsive UI and basic API tests.

## Security and approval boundaries

1. Never commit credentials, tokens, or environment files.
2. Use least-privilege tokens and read-only scopes for initial integrations.
3. Validate all webhook signatures before accepting events.
4. Record actor, timestamp, target, decision, and rationale for approval events.
5. Require explicit authenticated human approval before merging a pull request or deploying to production.
6. Verify CI, review requirements, and release checks from authoritative provider APIs; never infer success from a UI state.
7. Treat repository content, issue descriptions, comments, and CI logs as untrusted input.
8. Add authentication, authorization, CSRF protection, rate limits, and secret management before exposing this app beyond local development.

## Roadmap

### Milestone 1 — Registry and status dashboard
- [x] Project registry and basic dashboard.
- [x] Read-only GitHub/Jira snapshots.
- [x] Health endpoint and initial API tests.
- [ ] Execute automated tests in CI and confirm deployment configuration.

### Milestone 2 — Durable workflow model
- Add database migrations and persistent workflow/task/event tables.
- Define workflow states: planned, approved, running, waiting_for_review, blocked, failed, verified.
- Add idempotency keys, retry policies, cancellation, and per-step timeouts.
- Add append-only audit events and project-level permissions.

### Milestone 3 — Planning and implementation agents
- Convert an approved task into a structured plan with acceptance criteria and risk level.
- Require human approval for high-risk plans before execution.
- Run coding agents in isolated, ephemeral workspaces with resource and network controls.
- Keep secrets out of model prompts and logs.

### Milestone 4 — Verification and pull requests
- Run project-defined formatting, static analysis, tests, and security scans.
- Store check results, logs, artifact references, and commit SHA.
- Create pull requests only after checks pass; never merge automatically.
- Require human review and explicit approval for merge.

### Milestone 5 — Release verification
- Prepare release plans and rollback instructions.
- Require explicit human production-release approval.
- Deploy only through configured trusted pipelines.
- Verify health checks and deployment identity after release; report failures without claiming success.

## Local development

1. Create a virtual environment.
2. Install requirements.txt.
3. Copy .env.example to .env and set a strong FLASK_SECRET_KEY.
4. Run python app.py.
5. Run tests with pytest -q.

This MVP is not production-ready until authentication, CSRF protection, authorization, migrations, CI, and deployment-specific secret management are implemented.
