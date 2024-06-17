from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


async def write_data(session: AsyncSession, table: DeclarativeAttributeIntercept, data: list | dict) -> None:
    await session.execute(
        insert(table).values(data).on_conflict_do_nothing()
    )
    await session.commit()


async def delete_data(session: AsyncSession, table: DeclarativeAttributeIntercept, data_id: int, column) -> None:
    await session.execute(delete(table).filter(column == data_id))
    await session.commit()
