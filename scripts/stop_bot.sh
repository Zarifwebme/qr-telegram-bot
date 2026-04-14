#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ -f "bot.pid" ]] && ps -p "$(cat bot.pid)" >/dev/null 2>&1; then
  kill "$(cat bot.pid)"
  rm -f bot.pid
  echo "Bot to'xtatildi."
  exit 0
fi

if pkill -f "python.*bot.py" >/dev/null 2>&1; then
  rm -f bot.pid
  echo "Bot to'xtatildi (pattern bo'yicha)."
  exit 0
fi

echo "Ishlayotgan bot topilmadi."
