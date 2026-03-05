from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pathlib import Path

from app.core.logger import setup_logging, get_logger
from app.db.mongodb import MongoDB
from app.schemas.response import APIResponse, failure_response, success_response

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


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    if exc.status_code == 400:
        response = await failure_response(status_code=400, message=str(exc.detail))
        return JSONResponse(status_code=400, content=response.model_dump())

    response = await failure_response(status_code=500, message="Internal server error")
    return JSONResponse(status_code=500, content=response.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    response = await failure_response(
        status_code=422,
        message="Validation error",
        data={"errors": exc.errors()},
    )
    return JSONResponse(status_code=422, content=response.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception):
    response = await failure_response(status_code=500, message="Internal server error")
    return JSONResponse(status_code=500, content=response.model_dump())


@app.get("/", response_model=APIResponse)
async def root():
    logger.info("endpoint_called", endpoint="/")
    return await success_response(message="Hello World", data={})
