# Отдельный "сборочный" образ
FROM python:3.12-bookworm as compile-image

ARG MY_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.2


RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install $(test "$YOUR_ENV" == production && echo "--only=main") --no-interaction --no-ansi

COPY . /app/

CMD ["python", "-m", "bot"]