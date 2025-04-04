__all__ = [
    "User",
    "Address",
    "AddressType",
    "Membership",
    "Group",
]

from enum import StrEnum
from typing import List

from sqlalchemy import Enum, ForeignKey, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, CreatedUpdatedAtMixin, IdMixin


class User(Base, IdMixin, CreatedUpdatedAtMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    primary_address: Mapped["Address"] = relationship(
        back_populates="user",
        uselist=False,
        primaryjoin="and_(User.id==Address.user_id,Address.type=='PRIMARY')",
        overlaps="addresses",
        init=False,
    )
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        overlaps="primary_address",
        init=False,
    )
    groups: Mapped[List["Group"]] = relationship(
        secondary="memberships",
        back_populates="members",
        overlaps="memberships, user",
        init=False,
    )
    memberships: Mapped[List["Membership"]] = relationship(
        back_populates="user", overlaps="groups", init=False
    )


class AddressType(StrEnum):
    REGULAR = "REGULAR"
    PRIMARY = "PRIMARY"


class Address(Base, IdMixin, CreatedUpdatedAtMixin):
    __tablename__ = "addresses"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(
        back_populates="addresses", uselist=False, init=False
    )

    postal_code: Mapped[str] = mapped_column(String(20), nullable=True, default=None)
    country: Mapped[str] = mapped_column(String(100), nullable=True, default=None)
    city: Mapped[str] = mapped_column(String(100), nullable=True, default=None)
    street: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    address1: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    address2: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    type: Mapped[AddressType] = mapped_column(
        Enum(AddressType),
        insert_default=AddressType.REGULAR,
        server_default=text(f"'{AddressType.REGULAR.value}'"),
        default=None,
    )

    __table_args__ = (
        Index(
            "uq_user_primary_address",
            "user_id",
            unique=True,
            postgresql_where=(type == AddressType.PRIMARY),
        ),
    )


class Membership(Base, IdMixin, CreatedUpdatedAtMixin):
    __tablename__ = "memberships"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    user: Mapped["User"] = relationship(
        back_populates="memberships", overlaps="groups,memberships"
    )
    group: Mapped["Group"] = relationship(
        back_populates="memberships", overlaps="members,groups"
    )


class Group(Base, IdMixin):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

    members: Mapped[List["User"]] = relationship(
        secondary="memberships",
        back_populates="groups",
        overlaps="memberships,user",
        init=False,
    )
    memberships: Mapped[List["Membership"]] = relationship(
        back_populates="group", overlaps="members", init=False
    )
