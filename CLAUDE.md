# Resilient Channels — Adaptive Multi-Channel Router + Ops Dashboard

## Project Overview
Event-driven channel gateway routing customer interactions across voice, WhatsApp, USSD, and SMS with adaptive degradation and cross-channel session survival. Real-time React operations dashboard via GraphQL subscriptions. Targets 10M+ interactions/month across West Africa.

## Tech Stack
- Python 3.12+, mypy strict, ruff linter, async throughout
- FastAPI for channel gateway + GraphQL backend
- Strawberry GraphQL with subscriptions (WebSocket)
- Kafka (Redpanda for local dev) for event bus
- Redis for session state (30-min TTL)
- Prometheus client for metrics export
- TypeScript + React + Vite + recharts + Apollo Client for dashboard
- Docker + docker-compose for local dev
- Pydantic models for all data structures
- uv for Python package and project management

## Python Package Management — uv ONLY
IMPORTANT: Use uv exclusively. NEVER use pip, pip-tools, poetry, or conda directly.
- Install dependency: `uv add <package>`
- Install dev dependency: `uv add --dev <package>`
- Remove dependency: `uv remove <package>`
- Sync environment: `uv sync`
- Run any Python command: `uv run <command>`
- Run script: `uv run python script.py`
- Run tests: `uv run pytest tests/ -v`
- Run linter: `uv run ruff check src/ --fix`
- Run type checker: `uv run mypy src/ --strict`
- Run the app: `uv run python -m channels`
- NEVER run bare `python`, `pip`, `pytest`, `mypy`, or `ruff` — always prefix with `uv run`

## Package Layout
The Python package is named `channels` and lives under `src/channels/`.
pyproject.toml uses [tool.setuptools.packages.find] with where = ["src"].
uv.lock is committed to git for deterministic builds.
.python-version pins Python 3.12.
All imports use: `from channels.models import ...`, `from channels.session import ...`

## Commands
- `uv run ruff check src/ --fix` — lint + autofix
- `uv run mypy src/ --strict` — type check
- `uv run pytest tests/ -v` — run tests
- `uv sync` — install/sync all dependencies
- `docker-compose up` — start local stack
- `cd dashboard && npm run dev` — start React dashboard
- `uv run python -m benchmarks.chaos.runner --mode test` — run chaos test

## Project Structure (indented, not fenced)

    src/channels/
        adapters/          — Channel adapters (voice, whatsapp, ussd, sms)
            registry.py    — AdapterRegistry for cross-adapter lookups
            protocol.py    — ChannelAdapterProtocol interface
            normalizer.py  — Converts adapter-specific events to ChannelEvent
        session/           — Session manager + Redis state
            store.py       — Redis session store
            manager.py     — SessionManager with fallback logic
        events/            — Kafka producer/consumer + event schemas
        gateway/           — FastAPI app, routes, dependency injection
        graphql/           — Strawberry schema, subscriptions, resolvers
        agent/             — Stub agent orchestrator (simulated responses)
        models/            — Pydantic models shared across modules
        metrics/           — Prometheus counters and histograms
        utils/             — Phone hashing, cost constants, helpers
        config.py          — Settings via pydantic-settings
    dashboard/
        src/components/    — React dashboard widgets
        src/hooks/         — GraphQL subscription hooks + mock data
        src/graphql/       — GQL subscription/query documents
    infrastructure/        — Terraform modules
    k8s/                   — Kubernetes manifests
    tests/
        conftest.py        — Shared fixtures
    benchmarks/
        chaos/             — Chaos test framework
    docs/
        architecture.md    — System architecture with ASCII diagram
        cost-model.md      — Per-channel cost breakdown
        adr/               — Architecture Decision Records
    uv.lock                — Deterministic dependency lockfile (committed)
    .python-version        — Pins Python 3.12

## Conventions
- All async — never block the event loop
- Pydantic BaseModel for every data structure
- Kafka partition by session_id for ordering guarantee
- Phone numbers hashed with SHA-256 + salt in ALL events
    - Unhashed numbers only in Redis session store (ephemeral, 30-min TTL)
- USSD: 180s timeout, 160 char limit, CON/END response format
- All channel adapters implement ChannelAdapterProtocol
- ChannelType is Literal["voice", "whatsapp", "ussd", "sms"] — exactly 4 values
    - Voice fallback sends SMS with USSD shortcode; channel becomes "sms" with fallback_hint="ussd_shortcode_sent"
- Cost-per-channel constants defined once in src/channels/utils/costs.py

## Event Publishing Roles
- Channel Normalizer: publishes adapter-level events (session_started, message_received, channel_degraded)
- SessionManager: publishes lifecycle events (fallback_initiated, fallback_completed, session_resolved) with hash_phone()
- Both use EventProducer and ChannelEvent schema

## Logging
- structlog configured in config.py with JSON output

## Verification
- `uv run ruff check src/ --fix && uv run mypy src/ --strict && uv run pytest tests/ -v`

## Troubleshooting
- If mypy errors persist: check for circular imports between adapters/ and session/
- If Kafka consumer hangs: verify Redpanda with `docker-compose ps`
- If import errors: run `uv sync` to ensure environment is current
- If Claude uses bare `python` or `pip`: remind it to use `uv run` prefix
