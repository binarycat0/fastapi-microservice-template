__all__ = [
    "DemoModel",
    "ModelType",
]

import datetime
import decimal
import uuid
from enum import StrEnum

from sqlalchemy import (
    DECIMAL,
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    Float,
    Integer,
    String,
    text
)
from sqlalchemy.dialects.postgresql import JSONB, NUMERIC, REAL, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ModelType(StrEnum):
    PLAIN = "PLAIN"


class DemoModel(Base):
    __tablename__ = "demo_model"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default_factory=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        init=False,
    )

    col_int: Mapped[int] = mapped_column(Integer)
    col_float: Mapped[float] = mapped_column(REAL(precision=4, asdecimal=False))
    col_decimal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(precision=16, scale=4))
    col_bigint: Mapped[int] = mapped_column(BigInteger)
    col_str: Mapped[str] = mapped_column(String(255))
    col_bool: Mapped[bool] = mapped_column(Boolean)
    col_datetime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    col_updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    col_json: Mapped[dict | list] = mapped_column(JSONB(none_as_null=True))
    col_enum: Mapped[ModelType] = mapped_column(
        Enum(ModelType),
        default=ModelType.PLAIN,
        server_default=text(f"'{ModelType.PLAIN.value}'"),
    )
