#!/bin/bash

python -m gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.asgi:fastapi_app --bind 0.0.0.0:8000 --timeout 300 --log-level debug

exec "$@"
