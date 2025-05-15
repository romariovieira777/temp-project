FROM python:3.12-slim-bookworm AS base

FROM base AS builder

# Instala dependências de sistema necessárias para compilação
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    wget \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY uv.lock pyproject.toml /app/

# Instalar todas as dependências de uma vez
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/var/cache/apt \
    uv sync --frozen --no-dev && \
    uv pip install --no-deps psycopg[binary]

COPY src/ /app/src/
COPY main.py /app/main.py

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

# Instala o Google Chrome e o chromedriver
RUN apt-get update && \
    apt-get install -y chromium chromium-driver

FROM base

# Dependências de runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]