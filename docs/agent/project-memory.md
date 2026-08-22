# Project Memory

## Status on 2026-08-22

Blocks 1-3 from the GPT-5.4 setup session are complete. This repo is now ready for a focused feature-only follow-up session.

## Completed in this session

- backed up `.venv` to `.venv-py310-backup`
- created a fresh `.venv` with Python `3.12.14`
- bootstrapped `pip` in the new venv and upgraded it
- ran `scripts/setup_requirements.sh --dev` against the new venv
- manually installed `dograh-sdk 0.1.8` and `fish-audio-sdk 1.3.0`
- verified `pipecat` import from the repo-backed install
- verified session-local `codex --version` result is `0.149.0`
- created root `.env.example`
- created `docs/agent/*` handoff docs

## Still intentionally not done

- no Deepgram EU provider variant implementation
- no Fish Audio TTS provider implementation
- no enum, schema, factory, or UI dropdown changes for new providers
- no Pipecat feature code changes
- no emotion-tag wrapper implementation
- no unrelated refactors

## Important current facts

- `pipecat/` submodule commit remains `ca89ca3c2c2859aea6c5c7ead3d484f9472a2697`
- dirty files still exist in `examples/typescript/`
- global `openai` CLI entrypoint is currently broken at `/opt/homebrew/bin/openai`
- current repo metadata points to Python 3.13 even though this setup session targeted Python 3.12

## Before / After

| Area | Before | After |
| --- | --- | --- |
| venv | `.venv` on Python `3.10.20` | `.venv-py310-backup` preserved, fresh `.venv` on Python `3.12.14` |
| Pipecat | pip package blocked from newer versions by Python 3.10 | repo install via `scripts/setup_requirements.sh --dev`, import verified as `Pipecat 1.1.1.dev2026` |
| Codex | PATH conflict documented in handover | current session resolves `codex-cli 0.149.0` |
| Git | handover said Apple Git was active | current direct check used Homebrew `git version 2.55.0` |
| OpenAI | handover had package/path mismatch | venv package is `openai 2.54.0`; global CLI still fails with `ModuleNotFoundError: No module named 'openai.cli'` |
| `.env.example` | no root file | root `.env.example` added without secrets |
| Agent docs | absent | `docs/agent/` added with summary, decisions, memory, tools map, skills, and feature handoff |

## Follow-up guidance

The next session should start directly with feature implementation, but should respect the existing provider and service-factory patterns rather than inventing a parallel path.

## Deepgramm EU and Fish Audio implementation (2026-08-22)

- Added `deepgram_eu` as a separate STT provider titled `Deepgramm EU`, using `api.eu.deepgram.com`, the Flux v2 WebSocket URL, and fixed usage tags `dograh` and `eu`.
- Added Fish Audio as a TTS provider with an `s2-pro` default, manual voice reference ID, speed control, PCM output at the transport sample rate, and the existing XML function-tag filter.
- Reused the existing Deepgram key validator and added Fish Audio bearer-key validation without logging credentials.
- Added focused registry, validity, Nova/Flux routing, Fish PCM/settings, and eight S2 bracket-tag passthrough cases; 31 focused and provider-regression tests pass.
- The pinned `pipecat/` submodule was not changed. Its existing Deepgram custom endpoint/tag seams and Fish WebSocket service are used through `service_factory.py`.
- Regenerated `ui/src/client/` from the FastAPI OpenAPI endpoint after a one-time scoped `npm ci`; UI lint and production build pass, and the generated types contain `Deepgramm EU` and Fish Audio.
- Added ignored local `api/.env.test` with credential-free localhost service URLs so provider tests can source the documented test environment without using development or production configuration.
