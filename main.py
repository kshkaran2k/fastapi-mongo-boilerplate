from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.mongodb import MongoDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.init()
    yield
    await MongoDB.close()


app = FastAPI(title="FastAPI Mongo Boilerplate", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}
