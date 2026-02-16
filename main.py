from contextlib import asynccontextmanager
from fastapi import FastAPI
from pathlib import Path

from app.core.logger import setup_logging, get_logger
from app.db.mongodb import MongoDB

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

setup_logging(log_file="logs/app.log")
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup")
    await MongoDB.init()
    yield
    logger.info("shutdown")
    await MongoDB.close()


app = FastAPI(title="FastAPI Mongo Boilerplate", lifespan=lifespan)


@app.get("/")
async def root():
    logger.info("endpoint_called", endpoint="/")
    return {"message": "Hello World"}
