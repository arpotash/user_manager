import typing as t

import litestar

import src.exceptions as exceptions

ErrorT = t.TypeVar("ErrorT", bound=exceptions.ApiError)


def handle_custom_error(
    request: litestar.Request, exc: t.Generic[ErrorT]
) -> litestar.Response:
    return litestar.Response({"message": exc.message}, status_code=exc.status_code)
