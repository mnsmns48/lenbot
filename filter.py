from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import hv


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message):
        return (obj.from_user.id in hv.tg_bot_admin) == self.is_admin
