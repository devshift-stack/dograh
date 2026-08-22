# Core

- Dograh is a full-stack voice-AI platform: `api/` is the FastAPI backend, `ui/` the Next.js application and workflow builder, `pipecat/` a pinned git submodule for the realtime STT → LLM → TTS pipeline, `docs/` Mintlify documentation, `scripts/` contributor/deployment automation, and `sdk/` client SDK sources.
- Runtime state uses PostgreSQL, Redis/ARQ, and MinIO/S3-compatible storage.
- Backend API routes are mounted below `/api/v1`. Route handlers own HTTP/auth/response concerns; reusable orchestration belongs in `api/services/`; SQLAlchemy/session/query details belong in `api/db/`.
- Organization-scoped resources must be filtered or validated with `organization_id` for reads, lists, and foreign-key writes. A foreign-key constraint does not establish tenant ownership.
- Cross-worker mutations of in-memory state must propagate through `api/services/worker_sync/WorkerSyncManager`.
- `ui/src/client/` is generated from backend OpenAPI. Regenerate it; do not hand-edit generated client files.
- Provider changes follow existing schemas, configuration options, `api/services/pipecat/service_factory.py`, generated UI types/settings, and services in the repo-pinned Pipecat submodule. Never move the submodule to upstream HEAD as an incidental provider change.
- Dependency/runtime contracts and meaningful pins: `mem:tech_stack`.
- Daily setup, development, verification, migration, and generation commands: `mem:suggested_commands`.
- Backend, UI, documentation, and script-specific implementation rules: `mem:conventions`.