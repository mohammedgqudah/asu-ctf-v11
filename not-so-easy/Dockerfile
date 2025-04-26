FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

EXPOSE 8000

WORKDIR /app


RUN apt-get update && apt-get install -y socat
ADD . /app
RUN uv sync --frozen --no-dev

RUN uv add supervisor
COPY ./supervisord.conf /etc/supervisor/supervisord.conf

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
