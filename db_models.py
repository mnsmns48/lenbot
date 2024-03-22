import datetime
from sqlalchemy import DateTime, func, BigInteger
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Visitors(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=False), server_default=func.now())
    tg_id: Mapped[int] = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(nullable=True)
    tg_fullname: Mapped[str] = mapped_column(nullable=True)