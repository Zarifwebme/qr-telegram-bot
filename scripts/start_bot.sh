#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ ! -d ".venv" ]]; then
  echo "[ERROR] .venv topilmadi. Avval virtualenv yarating." >&2
  exit 1
fi

if [[ -f "bot.pid" ]] && ps -p "$(cat bot.pid)" >/dev/null 2>&1; then
  echo "Bot allaqachon ishlayapti (PID $(cat bot.pid))."
  exit 0
fi

nohup "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/bot.py" >> "$PROJECT_DIR/bot.log" 2>&1 &
echo $! > "$PROJECT_DIR/bot.pid"

echo "Bot ishga tushdi. PID: $(cat bot.pid)"
echo "Log: $PROJECT_DIR/bot.log"
