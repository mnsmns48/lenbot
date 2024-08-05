import asyncio
from typing import Union, Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, Update, CallbackQuery

from bot import dp
from config import engine


# class MediaGroupMiddleware(BaseMiddleware):
#     album_data: dict = {}
#
#     def __init__(self, latency: Union[int, float] = 0.1):
#         self.latency = latency
#
#     async def __call__(
#             self,
#             handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
#             message: Message,
#             data: dict[str, Any]
#     ) -> Any:
#         if not message.media_group_id:
#             await handler(message, data)
#             return
#         try:
#             self.album_data[message.media_group_id].append(message)
#         except KeyError:
#             self.album_data[message.media_group_id] = [message]
#             await asyncio.sleep(self.latency)
#             data['_is_last'] = True
#             data["album"] = self.album_data[message.media_group_id]
#             await handler(message, data)
#
#         if message.media_group_id and data.get("_is_last"):
#             del self.album_data[message.media_group_id]
#             del data['_is_last']
#
#
# class MediaMiddleware(BaseMiddleware):
#     def __init__(self, latency: Union[int, float] = 0.01):
#         self.medias = {}
#         self.latency = latency
#         super(MediaMiddleware, self).__init__()
#
#     async def __call__(
#             self,
#             handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
#             event: Union[Message, CallbackQuery],
#             data: Dict[str, Any]
#     ) -> Any:
#
#         if isinstance(event, Message) and event.media_group_id:
#             try:
#                 self.medias[event.media_group_id].append(event)
#                 return
#             except KeyError:
#                 self.medias[event.media_group_id] = [event]
#                 await asyncio.sleep(self.latency)
#
#                 data["album"] = self.medias.pop(event.media_group_id)
#
#         return await handler(event, data)


class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        if not message.media_group_id:
            await handler(message, data)
            return

        try:
            self.album_data[message.media_group_id].append(message)

        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]
            await handler(message, data)

        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data['_is_last']


@dp.update.middleware()
async def database_transaction_middleware(
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
) -> Any:
    async with engine.scoped_session() as session:
        data['session'] = session
        return await handler(event, data)
