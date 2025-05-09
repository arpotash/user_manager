import sqlalchemy.ext.asyncio as sa_io
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)

from src.config import config
from src.models import Base

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=config.DB_URL,
    before_send_handler="autocommit",
    session_config=session_config,
    create_all=True,
)
alchemy = SQLAlchemyPlugin(config=sqlalchemy_config)

AsyncPostgreSQLEngine = sa_io.create_async_engine(config.DB_URL, echo=config.DB_ECHO)
AsyncPostgreSQLSession = sa_io.async_sessionmaker(
    AsyncPostgreSQLEngine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=sa_io.AsyncSession,
)


async def get_db_connection(app):
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = AsyncPostgreSQLEngine
        app.state.engine = engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine
