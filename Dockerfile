FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps:
# - ffmpeg: required by pydub audio conversion
# - libgomp1: required by faiss-cpu wheels on manylinux
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy lock/config first for better build cache reuse.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY backend/ /app/

EXPOSE 8000

# Uvicorn for simplicity; swap to gunicorn later if needed.
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# uv run uvicorn main:app --host 0.0.0.0 --port 8000
