from fastapi import FastAPI
from joker_bot.web.api.economy.router.economy_router import router as economy_router

app = FastAPI()

app.include_router(economy_router)
