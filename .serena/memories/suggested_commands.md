# Suggested Commands

## Setup and daily development

```bash
git submodule update --init --recursive
source venv/bin/activate
./scripts/setup_requirements.sh --dev
bash scripts/start_services_dev.sh
cd ui && npm install
cd ui && npm run dev -- --hostname 0.0.0.0
bash scripts/stop_services.sh
tail -f logs/latest/*.log
```

- Preferred first-time setup is the repo devcontainer described in `docs/contribution/setup.mdx`; it prepares Postgres, Redis, MinIO, Python dependencies, env templates, and UI dependencies.
- Re-run `scripts/start_services_dev.sh` to restart backend services. It runs migrations, launches Uvicorn with reload plus ARQ/campaign/ARI processes, and waits for `/api/v1/health`.

## Tests and checks

```bash
source venv/bin/activate && set -a && source api/.env.test && set +a && python -m pytest api/tests/...
bash scripts/lint.sh
bash scripts/format.sh
pre-commit run --all-files
cd ui && npm test
cd ui && npm run build
```

- Backend tests must source `api/.env.test`, never `api/.env`.
- `scripts/lint.sh` runs mypy, Ruff checks, and Ruff format checks for `api/`.
- `scripts/format.sh` fixes selected Python imports/formatting in `api/` and `pipecat/`, then runs UI ESLint autofix.

## Generated artifacts and migrations

```bash
./scripts/makemigrate.sh "description"
./scripts/migrate.sh
cd ui && npm run generate-client
source venv/bin/activate && set -a && source api/.env && set +a && python -m scripts.dump_docs_openapi
```

- Regenerate the UI client after backend API/schema changes.
- Backend repo scripts use `api/.env`; test commands use `api/.env.test`.