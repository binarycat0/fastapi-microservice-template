from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column
)


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


class IdMixin(MappedAsDataclass):
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, init=False
    )


class CreatedUpdatedAtMixin(MappedAsDataclass):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        insert_default=datetime.now(UTC),
        server_default=text("(now() AT TIME ZONE 'UTC')"),
        init=False,
        default=None,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        insert_default=datetime.now(UTC),
        server_default=text("(now() AT TIME ZONE 'UTC')"),
        onupdate=datetime.now(UTC),
        init=False,
        default=None,
    )
