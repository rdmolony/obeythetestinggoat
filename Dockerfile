# syntax = docker/dockerfile:1.3
FROM python:3.7.12-slim-buster AS base
ENV PYTHONUNBUFFERED 1

WORKDIR /code
ADD requirements.txt /code/
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt
ADD . /code
VOLUME /code
