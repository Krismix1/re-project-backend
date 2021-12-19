FROM python:3.10.1-bullseye as build

# Create shared ENV VARs for setup and runtime
ENV POETRY_VERSION="1.1.12" \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  POETRY_NO_INTERACTION=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_NO_CACHE_DIR=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  SETUP_PATH="/opt/app"

# Add our to-be-created virtualenv to PATH
ENV PATH="$SETUP_PATH/.venv/bin:$PATH"
WORKDIR $SETUP_PATH

# Install all dependencies in cache-friendly way with Poetry, see:
#   https://github.com/python-poetry/poetry/issues/1301
COPY pyproject.toml poetry.lock ./
RUN python3 -m pip install "poetry==$POETRY_VERSION" && \
  poetry install --no-root --no-dev

COPY backend backend

# Runtime image
FROM python:3.10.1-slim-bullseye as runtime

ENV SETUP_PATH="/opt/app"
ENV PATH="$SETUP_PATH/.venv/bin:$PATH"
WORKDIR $SETUP_PATH

COPY --from=build $SETUP_PATH $SETUP_PATH

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5000"]
