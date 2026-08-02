from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.exceptions import global_exception_handler
from app.core.logger import logger
from app.core.middleware import logging_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Project Dumbo...")
    yield
    logger.info("Stopping Project Dumbo...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.middleware("http")(logging_middleware)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(router)
