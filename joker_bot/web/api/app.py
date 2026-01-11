import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True,
)

AI_SYSTEM_INSTRUCTION = Path("custom_ai_instruction.txt").read_text(encoding="utf-8")

from fastapi import FastAPI
from joker_bot.web.api.economy.router.economy_router import router as economy_router

app = FastAPI()

app.include_router(economy_router)
