import logging
import os
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True,
)

BASE_DIR = Path(__file__).resolve().parent
AI_SYSTEM_INSTRUCTION = os.environ["AI_INSTRUCTIONS"]

from fastapi import FastAPI
from joker_bot.web.api.economy.router.economy_router import router as economy_router
from joker_bot.web.api.ai.router.ai_router import router as ai_router
from joker_bot.web.api.user.router.user_router import router as user_router
from joker_bot.web.api.chat_storage.router.chat_storage_router import (
    router as chat_storage_router,
)

app = FastAPI()

app.include_router(economy_router)
app.include_router(ai_router)
app.include_router(user_router)
app.include_router(chat_storage_router)
