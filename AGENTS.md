# Dograh - Project Overview


## Serena
Relevant information about the project is in `.serena/memories`.
If Serena MCP tools are available, read them with `read_memory` (start at `core`).
Otherwise read the Markdown files under `.serena/memories/` with normal file tools.
Do not duplicate those facts into this file.

Dograh is a voice AI platform for building and deploying conversational AI agents with telephony and WebRTC support.

## Project Structure

```
dograh/
├── api/              # Backend - FastAPI application
├── ui/               # Frontend - Next.js application
├── scripts/          # Helper scripts for local development
├── docs/             # Mintlify documentation
├── pipecat/          # Pipecat framework (git submodule)
├── docker-compose.yaml       # Production/OSS deployment
├── docker-compose-local.yaml # Local development services
```

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: Next.js 15 with React 19, TypeScript, Tailwind CSS
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Cache/Queue**: Redis with ARQ for background tasks
- **Storage**: MinIO (S3-compatible) for audio files

## Local Development

Contributor setup and service startup are documented in `docs/contribution/setup.mdx`.

## Project Memory

Session-specific project memory for this fork lives in `docs/agent/`:

- `docs/agent/project-summary.md`
- `docs/agent/decisions.md`
- `docs/agent/project-memory.md`
- `docs/agent/tools-map.md`
- `docs/agent/skills.md`
- `docs/agent/FEATURE-HANDOFF.md`

Read these before starting new setup or provider work in this fork.

## Dograh Docs Routing

Use `https://docs.dograh.com/llms.txt` as the primary Dograh docs index before broad web search.

For provider work, prefer existing repo patterns plus the repo docs:

- `docs/configurations/transcriber.mdx` for STT provider expectations
- `docs/configurations/voice.mdx` for TTS provider expectations
- `docs/voice-agent/` for workflow-builder terminology and UI context

## Provider Implementation Guardrails

Before adding a provider variant or wiring new STT/TTS support:

- inspect existing implementations in `api/services/pipecat/service_factory.py`
- inspect schema and config shapes under `api/schemas/`
- inspect generated UI types and workflow settings under `ui/src/`
- inspect repo-pinned Pipecat services under `pipecat/src/pipecat/services/`

Do not blindly upgrade the `pipecat/` submodule to public upstream HEAD as part of routine provider work.

## Environment Configuration

- `api/.env` - Backend environment variables. Source this when running repo-owned backend scripts against the dev DB (e.g. `python -m scripts.dump_docs_openapi`).
- `api/.env.test` - Test-only environment variables. Source this when running pytest so tests hit the test DB and never the dev/prod credentials in `api/.env`.
- `ui/.env` - Frontend environment variables

Typical invocation:

```bash
# Tests
source venv/bin/activate && set -a && source api/.env.test && set +a && python -m pytest api/tests/...

# Backend scripts
source venv/bin/activate && set -a && source api/.env && set +a && python -m scripts.dump_docs_openapi
```
