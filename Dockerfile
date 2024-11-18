FROM python:3.11-slim
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

# Install project dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml /app/
RUN uv sync --no-dev

# Prepare entrypoint
ADD . /app/
RUN chmod +x scripts/*
ENTRYPOINT ["docker-entrypoint.sh"]
