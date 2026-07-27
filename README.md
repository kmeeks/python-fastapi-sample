# Python FastAPI Sample

A simple Todo list API built with FastAPI, SQLAlchemy, and SQLite. Sample code for testing agentic dev.

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000, with interactive docs at http://localhost:8000/docs.

## Project Structure

```
app/
├── main.py           # FastAPI app entrypoint
├── database/         # SQLAlchemy engine/session setup
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic request/response schemas
└── routers/          # API route definitions
```

## Development

```bash
uv run pytest      # run tests
uv run ruff check  # lint
uv run mypy .       # type check
```
