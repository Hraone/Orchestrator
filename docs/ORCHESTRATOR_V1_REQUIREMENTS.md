# Orchestrator V1 Requirements

**Status:** Approved scope baseline for implementation planning  
**Repository:** https://github.com/Hraone/Orchestrator  
**Jira project:** MIN  
**Version:** 1.0

## 1. Product goal

Orchestrator is a project-agnostic control plane where a user maps software projects, works with persistent role-based AI chats, approves requirements, coordinates Jira work, and audits the full delivery lifecycle. V1 prioritizes reliable traceability and human control over autonomous code execution. No feature may claim completion without recorded verification evidence.

## 2. Core entities

- **Project:** name, repository URL, Jira site/project key, configuration, timestamps.
- **Role:** role name, system instructions, provider/model assignment, enabled state.
- **Role chat:** exactly one persistent chat per project and role in V1; stable identity and durable message history.
- **Message:** author, content, timestamps, provider/model metadata, optional links to requirements, tickets, and actions.
- **Requirement:** Markdown content, source discussion references, version, status (draft, changes requested, approved, superseded), approver and timestamps.
- **Jira task link:** local project/task association, Jira issue key/URL, originating requirement and status snapshot.
- **Workflow handoff:** source role, destination role, requirement version, linked Jira tasks, context summary, status and timestamps.
- **Activity event:** actor (user/AI/system), action, target, timestamp, outcome, related IDs and sanitized details.
- **Verification record:** check name, result, evidence, commit/PR references and timestamp.
- **Merge/release record:** repository, PR URL/number, actual merge commit SHA, timestamp, approval and verification references.

## 3. Project mapping

Users manage multiple projects. Each project maps to a GitHub repository and a Jira project. Credentials stay server-side, never in browser code or committed files. Projects and data must remain isolated.

Acceptance criteria:
- Users can add, view, edit and archive/remove a project with confirmation for destructive actions.
- Repository URL and Jira project key are validated.
- Chats, requirements and events always reference the correct project.
- Provider tokens never appear in API responses or UI.

## 4. Persistent role-based chats

V1 default roles: Project Manager, Developer, QA/Tester, Reviewer. There is exactly one fixed chat per role per project. Reopening it loads the same durable conversation; it must not create a new chat. Role instructions and provider/model are configurable. Long histories are paginated and sending/loading/error states are visible.

Provider-agnostic adapter contract:
- Common interface accepts provider, model, role instructions, history and generation options.
- Adapters normalize text output, available usage metadata, rate limits, authentication errors and provider failures.
- Provider/model is selectable per role.
- Free-tier support is best-effort; quota failures are surfaced and must never silently trigger paid usage.
- API credentials are server-side secrets only.
- ChatGPT Go is not treated as API access. Review provider data-use terms before sending confidential data.

Acceptance criteria:
- The same project+role always resolves to the same chat ID.
- Messages survive refresh and later sessions.
- Provider changes do not erase history.
- Provider failures are visible and do not lose the user's message.

## 5. Requirement workflow and approval gate

1. User discusses a new need in Orchestrator.
2. Project Manager AI drafts a structured Markdown requirement using the discussion and linked project context.
3. Requirement is saved as a versioned draft linked to source messages.
4. User can inspect, edit, approve or request changes.
5. Only explicit approval of a specific version may trigger Jira task creation and downstream handoff.
6. Material changes after approval create a new version requiring re-approval before new downstream work.

Markdown requirement template includes title, project, version, status, source discussion, problem/goal, scope/non-goals, scenarios, functional requirements, testable acceptance criteria, dependencies, assumptions, risks, security/privacy, rollout/rollback notes, proposed Jira breakdown and approval history.

Acceptance criteria:
- Drafting never creates Jira issues.
- Approval records who approved which version and when.
- Requesting changes returns the requirement to revision status.
- Duplicate submissions are idempotent.
- Requirement versions and approval history remain auditable.

## 6. Jira task creation and handoff

After approval, create Jira tasks from the approved breakdown and store issue keys/URLs linked to requirement and discussion. Creation is idempotent. Partial failures show successes and allow safe retry without duplicates.

A handoff includes the approved requirement version, Jira issue links, relevant discussion summary/message links, previous role output, requested action, acceptance criteria and known risks. Handoffs are logged. V1 never auto-approves merges or production releases.

## 7. GitHub, verification, and merge records

V1 may read repository/PR metadata and store commit, pull request, test and merge references. Future write actions require least-privilege credentials and explicit authorization. A ticket is fixed only when authoritative status and required verification evidence support that claim. Merge ID must be an actual GitHub merge commit SHA or verified merge reference. Human approval is required before merge and production release.

## 8. Dashboard

Show:
- Project selector and mapped projects.
- All pending Jira tickets across projects with project, key, summary, status, assignee if available and Jira link.
- Last five verified fixed tickets, newest first, with project, Jira key, summary, verification result, PR link and actual merge ID when present.
- Recent activity with actor, action, target, timestamp, outcome and links.
- Workflows awaiting requirement approval or role handoff.
- Clear loading, empty, stale-data and integration-error states.

Do not fabricate metrics or show hardcoded demo statuses as real data.

## 9. Activity and audit log

Log project/config changes; role/provider/model changes without secret values; chat messages and AI outcomes; requirement drafts, revisions and approvals; Jira create/update attempts and results; handoffs; verification results; PR/commit/merge/release observations and approvals; and security-relevant events. Events are append-only for ordinary users. Correlation IDs trace discussion to requirement versions, Jira issues, PRs and merge records. Sanitize secrets and sensitive payloads.

## 10. Security and reliability

- Implement authentication before exposing multi-project data publicly.
- Enforce authorization and project-level isolation on every server endpoint.
- Use CSRF protection for cookie-authenticated actions.
- Validate inputs, constrain request sizes and apply rate limiting.
- Keep provider/Jira/GitHub secrets server-side with least privilege.
- Never expose stack traces or secrets to clients.
- Use durable storage for messages, requirements, approvals, tasks and events. Vercel filesystem and SQLite /tmp are not persistent storage.
- Add migrations, backup/restore plan, structured logs and health checks.
- Make external side effects idempotent and safe to retry.
- Record quota/rate-limit failures and never silently incur paid charges.

## 11. Suggested technical direction

Keep Flask where practical. Use durable PostgreSQL (Supabase PostgreSQL is a candidate) for persistent entities. Use provider adapters for AI APIs. Keep API contracts explicit. Deploy on Vercel only if persistence, runtime and background-work patterns are compatible; otherwise select a suitable Python host. Hosting must not compromise data durability.

## 12. V1 non-goals

- Fully autonomous production deployment.
- Automatic merge/release without human approval.
- Unlimited AI usage or guaranteed free inference.
- Treating ChatGPT Go as API access.
- Arbitrary unvalidated role workflows.
- Claiming completion without authoritative verification.
- Enterprise billing/analytics complexity.

## 13. Delivery phases and acceptance gates

### Phase 1 — Foundation
Authentication, durable schema/migrations, project mapping, role definitions, provider configuration and secret handling.

**Gate:** authenticated users can create isolated projects; secrets do not leak; migrations and tests pass.

### Phase 2 — Persistent chats and provider adapters
Fixed chat per project+role, message history, provider abstraction, configurable model per role, quota/error handling.

**Gate:** chat identity stays stable; history persists; tests cover success, timeout, invalid credentials and quota/rate limits.

### Phase 3 — Requirements and approval
Project Manager drafting, versioned Markdown, edit/revise/approve controls and audit trail.

**Gate:** no Jira tasks before explicit approval; approval ties to an exact version.

### Phase 4 — Jira and handoffs
Task breakdown, idempotent issue creation, links, role handoffs and activity events.

**Gate:** retries do not duplicate tasks; partial failures recover; tasks trace back to requirement and discussion.

### Phase 5 — Dashboard and GitHub verification
Pending Jira list, last five verified fixed tickets with real merge IDs, recent activity, verification and approval status.

**Gate:** items come from actual integrations/database; missing merge IDs remain missing.

### Phase 6 — Hardening and deployment
Security review, responsive UX, error states, logging, backups and deployment verification.

**Gate:** automated tests and security checks pass; health and live smoke tests validate critical workflows.

## 14. Definition of done

A feature is complete only when acceptance criteria are documented, tests pass, errors are handled, data is persisted durably, relevant audit events exist, and deployed behavior is verified. Do not mark tickets fixed merely because code was committed.
