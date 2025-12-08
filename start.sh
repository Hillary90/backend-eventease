#!/usr/bin/env bash
set -euo pipefail

# If a Firebase service account is provided via env, write it to serviceAccountKey.json
if [ -n "${FIREBASE_SERVICE_ACCOUNT_BASE64:-}" ]; then
  echo "Writing serviceAccountKey.json from FIREBASE_SERVICE_ACCOUNT_BASE64"
  echo "$FIREBASE_SERVICE_ACCOUNT_BASE64" | base64 --decode > serviceAccountKey.json
  chmod 600 serviceAccountKey.json
elif [ -n "${FIREBASE_SERVICE_ACCOUNT:-}" ]; then
  echo "Writing serviceAccountKey.json from FIREBASE_SERVICE_ACCOUNT"
  printf '%s' "$FIREBASE_SERVICE_ACCOUNT" > serviceAccountKey.json
  chmod 600 serviceAccountKey.json
else
  echo "No Firebase service account provided via env. Continuing without it."
fi

# Start Gunicorn with Uvicorn worker (respect $PORT if set)
PORT=${PORT:-8000}
exec gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:${PORT} --workers 1
