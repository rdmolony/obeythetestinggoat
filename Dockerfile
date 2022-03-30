# syntax = docker/dockerfile:1.3
FROM python:3.7.12-slim-buster AS base

# -> PYTHONUNBUFFERED ensures that python output is sent straight to the terminal
# so that we can see the output of this application (e.g. django logs) in real time
# -> PATH adds the virtualenv’s bin/ directory to the start of the list of directories
# which are searched for commands to run SO don't have to activate it during each RUN 
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv 

WORKDIR /app/

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.1.11
RUN --mount=type=cache,target=/root/.cache \
    pip install "poetry==$POETRY_VERSION"
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY pyproject.toml poetry.lock /app/
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-interaction && \
    pip install selenium==3 fabric # workaround as cryptography fails to install via poetry
VOLUME /app/
