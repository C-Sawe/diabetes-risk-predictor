#!/usr/bin/env bash
# Launch both the API (:8000) and the dashboard (:5173) for a live demo.
# Ctrl-C stops both. Run once from the project root: ./start.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="/opt/homebrew/bin:$PATH"

echo "starting API on :8000"
(
  cd "$ROOT/backend"
  source venv/bin/activate
  uvicorn api.main:app --port 8000
) &
API_PID=$!

echo "starting dashboard on :5173"
(
  cd "$ROOT/frontend"
  npm run dev
) &
WEB_PID=$!

trap 'kill $API_PID $WEB_PID 2>/dev/null' EXIT
wait
