from collections.abc import AsyncGenerator

from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.external_systems.db import AsyncPostgreSQLSession


async def provide_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncPostgreSQLSession() as session:
        try:
            async with session.begin():
                yield session
        except IntegrityError as exc:
            raise ClientException(
                status_code=HTTP_409_CONFLICT, detail=str(exc)
            ) from exc
        except Exception as e:
            raise e
