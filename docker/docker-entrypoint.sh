#!/usr/bin/env bash
set -eu

python -m alembic upgrade head

# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
# must read port value from env vars
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:=5000}
