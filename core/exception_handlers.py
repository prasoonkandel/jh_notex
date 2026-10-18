from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:

    if not isinstance(exception, RequestValidationError):
        raise exception

    error = exception.errors()[0]

    if error["type"] == "value_error":
        message = str(error["ctx"]["error"])
    else:
        message = error["msg"]

    return JSONResponse(
        status_code=422,
        content={"detail": message},
    )
