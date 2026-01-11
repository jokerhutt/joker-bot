import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True,
)

BASE_DIR = Path(__file__).resolve().parent
AI_SYSTEM_INSTRUCTION = (BASE_DIR / "custom_ai_instructions.txt").read_text(
    encoding="utf-8"
)

from fastapi import FastAPI
from joker_bot.web.api.economy.router.economy_router import router as economy_router
from joker_bot.web.api.ai.router.ai_router import router as ai_router
from joker_bot.web.api.user.router.user_router import router as user_router

app = FastAPI()

app.include_router(economy_router)
app.include_router(ai_router)
app.include_router(user_router)
