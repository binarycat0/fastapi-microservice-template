import datetime
import uuid
from enum import StrEnum

from sqlalchemy import String, Boolean, DateTime, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from .base import Base

class ModelType(StrEnum):
    PLAIN = "PLAIN"

class DemoModelChild(Base):
    __tablename__ = "demo_model_child"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )

    model: Mapped["DemoModel"] = relationship("DemoModel")

class DemoModel(Base):
    __tablename__ = "demo_model"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )

    col_str: Mapped[str] = mapped_column(
        String(255)
    )
    col_bool: Mapped[bool] = mapped_column(
        Boolean
    )
    col_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True)
    )
    col_updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True)
    )
    col_json: Mapped[dict] = mapped_column(
        JSONB(none_as_null=True)
    )
    col_enum: Mapped[ModelType] = mapped_column(
        Enum(ModelType), default=ModelType.PLAIN, server_default=text(f"'{ModelType.PLAIN.value}'")
    )

    children: Mapped[list[DemoModelChild]] = relationship(
        DemoModelChild
    )
