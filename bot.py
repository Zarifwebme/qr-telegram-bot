"""Project entrypoint for local runs and Procfile workers."""

from __future__ import annotations

import asyncio

from app.bot import main


if __name__ == "__main__":
    asyncio.run(main())