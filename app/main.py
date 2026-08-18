from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router
from app.database.init_db import create_admin
from app.exceptions.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_admin()
    yield


app = FastAPI(
    title="Book Store API",
    description="REST API for a book store",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)

register_exception_handlers(app)
