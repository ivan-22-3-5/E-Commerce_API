from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.db import models
from src.db.db import engine
from src.routers import auth, users, orders, products, categories, reviews, addresses
from src.custom_exceptions import (
    ECommerceApiError,
    ResourceDoesNotExistError,
    ResourceAlreadyExistsError,
    NotEnoughRightsError,
    InvalidTokenError,
    InvalidCredentialsError,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(reviews.router)
app.include_router(addresses.router)


def create_exception_handler(status_code, initial_detail) -> Callable[[Request, ECommerceApiError], JSONResponse]:
    async def exception_handler(_: Request, exc: ECommerceApiError) -> JSONResponse:
        content = {"detail": initial_detail}
        if exc.message:
            content["detail"] = exc.message
        return JSONResponse(status_code=status_code, content=content, headers=exc.headers)
    return exception_handler


app.add_exception_handler(
    exc_class_or_status_code=ResourceDoesNotExistError,
    handler=create_exception_handler(status.HTTP_404_NOT_FOUND, "Resource not found")
)

app.add_exception_handler(
    exc_class_or_status_code=ResourceAlreadyExistsError,
    handler=create_exception_handler(status.HTTP_409_CONFLICT, "Resource already exists")
)

app.add_exception_handler(
    exc_class_or_status_code=NotEnoughRightsError,
    handler=create_exception_handler(status.HTTP_403_FORBIDDEN, "Not enough rights to execute the operation")
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidTokenError,
    handler=create_exception_handler(status.HTTP_401_UNAUTHORIZED, "Ivalid token")
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidCredentialsError,
    handler=create_exception_handler(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
)
