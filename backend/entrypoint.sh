#!/bin/bash
set -e

# Activate virtual environment if you're using one
# source /path/to/venv/bin/activate

# Run database migrations if needed
# alembic upgrade head

# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000