FROM ubuntu:20.04

ENV LANG="C.UTF-8" LC_ALL="C.UTF-8" PATH="/home/python/.poetry/bin:/home/python/.local/bin:$PATH" PIP_NO_CACHE_DIR="false"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python-is-python3 curl ca-certificates wait-for-it libpq-dev python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 python && \
    useradd  --uid 1000 --gid python --shell /bin/bash --create-home python

USER 1000
RUN mkdir /home/python/app
WORKDIR /home/python/app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/d3c9049a18ae33baacfcb5c698777282f2f58128/get-poetry.py | python
RUN poetry config virtualenvs.create false

COPY --chown=python:python pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root --ansi

COPY --chown=python:python . .
RUN poetry install --no-interaction --ansi

CMD ["usedgoodreads"]
