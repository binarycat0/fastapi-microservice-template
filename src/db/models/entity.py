from enum import StrEnum

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from .base import Base, CreatedUpdatedAtMixin, IdMixin
from .users import User

__all__ = ["Entity"]


class Entity(Base, IdMixin, CreatedUpdatedAtMixin):
    __tablename__ = "entities"

    class Type(StrEnum):
        DUMMY = "DUMMY"
        WORKSPACE = "WORKSPACE"
        NAMESPACE = "NAMESPACE"
        TABLE = "TABLE"

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped[User] = relationship(
        back_populates="entities", uselist=False, init=False
    )

    type: Mapped[Type] = mapped_column(
        Enum(Type),
        insert_default=Type.DUMMY,
        server_default=text(f"'{Type.DUMMY.value}'"),
    )
    name: Mapped[str] = mapped_column(String(255), nullable=True, insert_default=None)
    description: Mapped[str] = mapped_column(
        String(255), nullable=True, insert_default=None
    )
    properties: Mapped[dict] = mapped_column(
        JSONB(none_as_null=True),
        nullable=True,
        insert_default=dict,
        server_default=text("'{}'::jsonb"),
    )
