ARG TARGETPLATFORM=linux/amd64
FROM --platform=$TARGETPLATFORM python:3.11.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    PORT=8000 \
    WORKERS=1 \
    UVICORN_APP=app.main:app 

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gcc \
   && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

RUN useradd -m -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

COPY --chown=appuser:appuser app ./app

EXPOSE 8000
CMD ["sh", "-c", "uvicorn ${UVICORN_APP} --host 0.0.0.0 --port ${PORT} --workers ${WORKERS}"]
