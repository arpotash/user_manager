from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig

from advanced_alchemy.extensions.litestar import (
    SQLAlchemyInitPlugin,
    SQLAlchemySerializationPlugin,
)
from src.dependencies.session import provide_session
from src.exceptions import ApiError
from src.extensions import handle_custom_error
from src.external_systems.db import get_db_connection, sqlalchemy_config
from src.routers.user import UserController

plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    engine = await get_db_connection(app)
    try:
        yield
    finally:
        await engine.dispose()


app = Litestar(
    [UserController],
    dependencies={"session": provide_session},
    lifespan=[
        lifespan,
    ],
    openapi_config=OpenAPIConfig(
        title="My API",
        description="This is the description of my API",
        version="0.1.0",
        path="/docs",
    ),
    exception_handlers={ApiError: handle_custom_error},
    plugins=[SQLAlchemySerializationPlugin(), SQLAlchemyInitPlugin(sqlalchemy_config)],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
