# Development Orchestrator

A project-agnostic control plane for coordinating software delivery across repositories and issue trackers.

## Goals

- Register multiple projects and their GitHub/Jira connections.
- Show project, issue, repository, and delivery status in one dashboard.
- Evolve toward controlled planning, implementation, test execution, pull-request preparation, and release verification.
- Keep merge and production-release actions behind explicit human approval.

## Safety boundaries

- Never store access tokens in source control; use environment variables or a secrets manager.
- Start integrations read-only until permission scopes and approval flows are reviewed.
- Do not merge pull requests or release to production automatically.
- Do not report work as complete unless required checks have actually passed.

## MVP status

The initial milestone is a responsive dashboard, project registry, and read-only GitHub/Jira status snapshots. Workflow execution, CI orchestration, approval gates, audit logs, and release verification will follow as separate milestones.

## Local development

The application scaffold and setup instructions will be added in the initial implementation commit.