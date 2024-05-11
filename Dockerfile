FROM python:3.10.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
    dumb-init \
    curl \
    lsof \
    && apt-get clean


# download requirements from pipenv
FROM base as python-deps

RUN pip install --upgrade pip && pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY Pipfile.lock .
COPY Pipfile .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy && pipenv install flake8 isort black


#build project
FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY . .

EXPOSE 8000

# доделать чтобы автоматически делались миграции
ENTRYPOINT chmod +x alembic.ini && dumb-init alembic -c alembic.ini upgrade head && python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --access-log --log-config src/logging.conf