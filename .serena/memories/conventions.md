# Conventions

## Backend

- Keep routes limited to validation, authentication/organization resolution, and response shaping. Put reusable or multi-step business logic and external calls in the owning `api/services/<domain>/` module; do not create pass-through services or catch-all modules.
- Routes, services, tasks, and MCP code call DB clients. Only `api/db/` owns direct SQLAlchemy imports, sessions, query construction, loading choices, and transactions.
- Enforce tenant isolation in the query/lookup itself with `organization_id`; validate referenced org-scoped rows before assigning foreign keys.
- Use `WorkerSyncManager` for state changes that every FastAPI worker must observe.
- Pytest discovers `test_*.py` and `*_test.py`; async tests use pytest-asyncio auto mode.

## Frontend

- Use Next.js App Router and strict TypeScript. `@/*` resolves to `ui/src/*`.
- Do not edit generated files in `ui/src/client/`; use `npm run generate-client`.
- Authenticated fetch effects must wait until `useAuth()` is no longer loading and a user exists.
- Generated API calls resolve to `{ data, error }` on HTTP failures. Check `response.error` and normalize it with `detailFromError`; `try/catch` covers only network/runtime failures.
- File uploads use a hidden native file input triggered by a visible button, with the chosen filename displayed.
- ESLint requires sorted imports/exports, no unused imports, trailing spaces, or excessive blank lines.

## Scripts and docs

- Keep contributor-facing Bash/PowerShell pairs behaviorally equivalent: env names, defaults, flags, and workflow must change together.
- Treat deployment scripts, `scripts/lib/setup_common.sh`, Compose profiles, and `deploy/templates/` as a coupled system; `.env` remains operator-owned configuration.
- Bash libraries sourced by other scripts must not impose shell options on callers; executable entrypoints may use strict mode.
- Mintlify pages are MDX with YAML `title` and `description`; use second person, prerequisites before procedures, language-tagged tested examples, image alt text, and relative internal links.
- Keep secrets and credentials out of source, examples, diffs, logs, docs, and memories.