FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

WORKDIR /app

ADD . /app
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 3000

ENTRYPOINT []
CMD ["sh", "-c", "uv run main.py"]
