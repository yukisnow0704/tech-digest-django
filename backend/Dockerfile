FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY . .
RUN SECRET_KEY=build DATABASE_URL=sqlite:// python manage.py collectstatic --noinput

CMD exec gunicorn config.wsgi --bind :$PORT --workers 2 --threads 4 --timeout 60