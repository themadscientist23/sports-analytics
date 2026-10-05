# Sports Analytics Platform

Custom Elo ("CatElo") ratings for NBA, NFL, and MLB. FastAPI + MySQL backend, React frontend. Work in progress.

## Done

- fastAPI backend with endpoints for seasons, standings and team rating history
- mySQL via SQLAlchemy, with per-sport models (NBA, NFL, MLB) built on shared base classes
- game ingest from balldontlie: full-season backfill and a daily update
- rating pipeline per sport, reset each season
- react frontend with standings and team pages
- backend organized as an `app` package, with env settings in `core/` and dependency-injected DB sessions
- alembic migrations for the schema
- ruff linting and a pytest setup
- seasons tagged on every game
- `pydantic-settings` for config and logging instead of prints
- daily cron script that runs from any path
- frontend cleanup: one API base URL, loading and error states, accessible links and sort buttons

## ToDo

- backfill and rate every sport
- season picker
- tune CatElo per sport (placeholder right now)
- more tests
