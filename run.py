from app.config.settings import Config

if Config.MODE == "server":
    if __name__ == "__main__":
        import uvicorn

        uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
