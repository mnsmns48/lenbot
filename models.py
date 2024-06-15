from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, BigInteger, Sequence, BIGINT, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Visitors(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=False), server_default=func.now())
    tg_id: Mapped[int] = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(nullable=True)
    tg_fullname: Mapped[str] = mapped_column(nullable=True)


class Posts(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=Sequence('posts_id_seq', start=1))
    post_id: Mapped[int | None] = mapped_column(BigInteger)
    time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=False), server_default=func.now())
    group_id: Mapped[int | None] = mapped_column(BigInteger)
    group_name: Mapped[str | None]
    signer_id: Mapped[int | None] = mapped_column(BigInteger)
    signer_name: Mapped[str]
    phone_number: Mapped[int | None] = mapped_column(BigInteger)
    text: Mapped[str | None] = mapped_column(Text)
    is_repost: Mapped[bool | None]
    repost_source_id: Mapped[int | None] = mapped_column(BigInteger)
    repost_source_name: Mapped[str | None]
    attachments: Mapped[str | None]
    source: Mapped[str | None]


class LeninoWork(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True)
    title: Mapped[str]
    author: Mapped[Optional[str]]
    payment: Mapped[str]
    cond: Mapped[str]
    desc: Mapped[str] = mapped_column(Text)
    performance: Mapped[str]
    locality: Mapped[str]
    link: Mapped[str]
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False))


class PreModData(Base):
    __tablename__ = 'premoderate'
    date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    url: Mapped[str]
    source: Mapped[str]
    internal_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    source_id: Mapped[int | None] = mapped_column(BIGINT)
    source_title: Mapped[str | None]
    signer_id: Mapped[int | None] = mapped_column(BIGINT)
    signer_name: Mapped[str | None]
    phone_number: Mapped[int | None] = mapped_column(BIGINT)
    text: Mapped[str | None] = mapped_column(Text)
    is_repost: Mapped[bool | None]
    repost_source_id: Mapped[int | None] = mapped_column(BIGINT)
    repost_source_title: Mapped[str | None]
    attachments_info: Mapped[str | None]
    attachments: Mapped[dict | None] = mapped_column(type_=JSON)
