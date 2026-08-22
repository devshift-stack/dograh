# Tech Stack

## Backend

- Python metadata: root `.python-version` pins 3.13.7; `api/pyproject.toml` requires `>=3.13,<3.14`. The dependency bootstrap script accepts Python 3.12 or 3.13, but project metadata is the authoritative target for normal development.
- FastAPI backend with Pydantic schemas, async SQLAlchemy persistence, Alembic migrations, Redis-backed ARQ workers, PostgreSQL, and MinIO/S3-compatible object storage.
- Dependencies are declared in `api/requirements.txt` and `api/requirements.dev.txt`, installed with `uv pip`; tests use pytest, lint/format use Ruff, and type checking uses mypy.
- Pipecat is a git submodule installed editable with selected provider extras; submodule compatibility takes precedence over public upstream HEAD.

## Frontend

- `ui/.nvmrc` pins Node v24.11.1.
- Next.js 15 App Router, React 19, strict TypeScript 5, Tailwind CSS 4, shadcn/Radix primitives, Zustand state, and `@xyflow/react` for workflow graphs.
- npm with `ui/package-lock.json`; Vitest for tests; ESLint 9 flat config; OpenAPI client generation via `@hey-api/openapi-ts`.

## Other

- Mintlify MDX documentation configured by `docs/docs.json`.
- Docker Compose supplies local/runtime services; contributor setup prefers the VS Code devcontainer.
- Bash scripts cover macOS/Linux; paired PowerShell scripts cover Windows contributor workflows.