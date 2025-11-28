# Solar AI Backend Structure

This guide explains how the backend modules are organized so you can quickly find the APIs that serve logged-in teams, AI agents, and proposal generation.

## Key folders

- `app/main.py` wires FastAPI with CORS and mounts these routers:
  - `app/auth/router.py` handles `/auth/signup` and `/auth/login` with SQLAlchemy users and JWT tokens.
  - `app/routers/health.py` exposes `/health` for uptime monitoring.
  - `app/routers/leads.py` is the primary logged-in surface for leads, AI summaries, proposal PDFs, and future AI actions (roof analysis, proposal regeneration).
  - `app/routers/chat.py` currently returns placeholder AI replies, making it a natural place to expand lead-generation chatbots or quoting assistants.

- `app/ai.py` contains shared AI logic (system size math, `generate_ai_summary`). Update the missing `prompt` definition to tailor it to solar quoting, AHJ lookups, or plan reviews.
- `app/database.py` initializes the Supabase client used by `leads.py` for storing/retrieving logged-in user leads. The `app/db.py`, `app/models/`, and `app/schemas/` packages can stay ready for SQLAlchemy-based sales CRM tables.
- `app/pdf_generator.py` holds the proposal export helper invoked when leads are created or regenerated.
- `app/utils.py` stores helpers such as `detect_utility_from_address`, useful for AHJ or customer quoting assistants.
- `app/auth/` includes `dependencies.py`, `models.py`, `schemas.py`, `router.py`, and `utils.py` so authentication logic lives in one place.
- `app/routers/agents/` does not exist yet but can be added to group new capabilities (AHJ finder, plan review, quoting assistant) alongside `leads.py`.
- `proposals/` is the current landing spot for generated proposal PDFs (ensure it is writable and listed in `.gitignore` if files should not be committed).

## Logged-in user workflow

1. The frontend hits `/auth/login` to obtain JWTs (handled by the SQLAlchemy user model and tokens via `app/auth/utils.py`).
2. Authenticated requests (protected via Next.js middleware) call `/leads/` to fetch/add leads and download proposals.
3. Each lead creation triggers:
   - `calculate_system_size` (tariff-based sizing),
   - `generate_ai_summary` (OpenAI),
   - PDF generation from `app/pdf_generator`,
   - Supabase updates with paths for retrieval.
4. `/chat/` and future `/agents/*` endpoints can share the same AI helper functions and assist with AHJ lookup, plan review, or quoting logic.

## Suggestions

- If you expect multiple AI agent flows, add `app/routers/agents/` with individual modules (`ahj.py`, `plan_review.py`, `quote.py`) and include them in `main.py`.
- Keep `app/database.py` and `app/db.py` synchronized: choose either Supabase or SQLAlchemy as your primary store to avoid duplication.
- Document in this folder how to run `uvicorn` with the `.env` file so new developers can start the backend quickly.

Let me know if you’d like me to implement any of these structural updates (new routers, docs, middleware cleanup) as well.