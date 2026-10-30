import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT

from core.exception_handlers import validation_exception_handler
from routers.auth import router as auth_router
from routers.note import router as note_router
from routers.share import router as share_router
from routers.user import router as user_router

app = FastAPI(
    title="JingHua Notex API",
    version="0.1.0",
)

origins = []

for origin in os.getenv("CORS_ORIGINS", "").split(","):
    if origin.strip():
        origins.append(origin.strip().rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(note_router)
app.include_router(share_router)


@app.get("/")
async def root():
    return {"message": "Welcome to JingHua Notex"}


app.add_exception_handler(RequestValidationError, validation_exception_handler)
