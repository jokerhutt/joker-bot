import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "joker_bot.web.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
