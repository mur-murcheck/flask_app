#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

mkdir -p logs
LOG_FILE="logs/api.log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] - \e[1;32m[INFO]\e[0m Starting API gateway"

if [[ ! -d .venv ]]; then
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] - \e[1;31m[ERROR]\e[0m .venv not found. Run: python3 -m venv .venv && pip install -r requirements.txt"
  exit 1
fi

. .venv/bin/activate

export FLASK_APP=app:app

exec flask run --host=0.0.0.0 --port=8080 --debug
