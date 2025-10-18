from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.mongodb import MongoDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Startup
    await MongoDB.init()
    yield
    # On Shutdown
    await MongoDB.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}