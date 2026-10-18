import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT

from routers.auth import router as auth_router
from routers.note import router as note_router
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


@app.get("/")
async def root():
    return {"message": "Welcome to JingHua Notex"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    error = exception.errors()[0]

    field = str(error["loc"][-1]).replace("_", " ").capitalize()
    error_type = error["type"]

    if error_type == "string_too_short":
        length = error["ctx"]["min_length"]
        message = f"{field} should have at least {length} characters"

    elif error_type == "string_too_long":
        length = error["ctx"]["max_length"]
        message = f"{field} should have at most {length} characters"

    elif error_type == "missing":
        message = f"{field} is required"

    else:
        message = f"{field}: {error['msg']}"

    return JSONResponse(
        status_code=422,
        content={"detail": message},
    )
