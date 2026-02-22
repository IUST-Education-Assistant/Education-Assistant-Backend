FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps:
# - ffmpeg: required by pydub audio conversion
# - libgomp1: required by faiss-cpu wheels on manylinux
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

# Uvicorn for simplicity; swap to gunicorn later if needed.
#  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# entered this in hamravesh
# /bin/bash -c "uvicorn main:app --host 0.0.0.0 --port 8000"