import os
from asyncio import current_task
from contextlib import asynccontextmanager
from pathlib import Path

from pydantic import SecretStr
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session

from pydantic_settings import BaseSettings

root_path = Path(os.path.abspath(__file__)).parent


class Settings(BaseSettings):
    tg_bot_admin: list[int]
    editor_admin: int
    tg_chat_id: str
    bot_token: SecretStr
    db_username: str
    db_password: SecretStr
    db_port: int
    db_name: str
    dobrotsen_db_name: str
    notification: bool


class BotImages(BaseSettings):
    main_page_image: str
    suggest_post: str
    admin_img: str
    work_img: str
    search_number: str
    dobrotsen_img: str


hv = Settings(_env_file=f"{root_path}/.env")
_img = BotImages(_env_file=f"{root_path}/pictures.env")


class CoreConfig():
    def __init__(self, db):
        self.db = db
        self.base: str = (
            f"postgresql+asyncpg://{hv.db_username}:{hv.db_password.get_secret_value()}"
            f"@localhost:{hv.db_port}/{db}"
        )
        self.db_echo: bool = False


dbconfig = CoreConfig(db=hv.db_name)
dobrotsen_config = CoreConfig(db=hv.dobrotsen_db_name)


class AsyncDataBase:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url.replace('driver', 'asyncpg'),
            echo=echo,
            poolclass=NullPool
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        try:
            async with session() as s:
                yield s
        finally:
            await session.remove()

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = await self.scoped_session()
        yield session
        await session.close()


engine = AsyncDataBase(dbconfig.base, dbconfig.db_echo)
dobro_engine = AsyncDataBase(dobrotsen_config.base, dobrotsen_config.db_echo)
