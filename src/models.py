import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from passlib.context import CryptContext

metadata = sa.MetaData()
Base = orm.declarative_base(metadata=metadata)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class MetaOrm:
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )


class User(Base, MetaOrm):
    __tablename__ = "user"
    __table_args__ = (sa.UniqueConstraint("name", "surname", name="uniq_name_surname"),)

    id: orm.Mapped[int] = orm.mapped_column(
        sa.BIGINT,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор пользователя",
    )
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(length=64), nullable=False, comment="Имя пользователя"
    )
    surname: orm.Mapped[str] = orm.mapped_column(
        sa.String(length=64), nullable=False, comment="Фамилия пользователя"
    )
    password: orm.Mapped[str] = orm.mapped_column(
        sa.String(length=128), nullable=False, comment="Пароль"
    )

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
