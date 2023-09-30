# Based on:
# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

FROM python:3.11-buster as build

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR='/tmp/poetry_cache'

WORKDIR /app

COPY poetry.lock pyproject.toml README.md ./

RUN poetry install --no-root --without dev && rm -rf $POETRY_CACHE_DIR

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1

COPY --from=build $VIRTUAL_ENV $VIRTUAL_ENV

COPY pybetter pybetter

WORKDIR /src

ADD . .

ENTRYPOINT ["python3", "-m", "pybetter"]
