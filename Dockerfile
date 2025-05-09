# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.5
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH="${PYTHONPATH}:/app/src"


WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root --no-cache
RUN poetry run pip list

COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["poetry", "run", "python", "src/app.py"]
