from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog

from dialog_admin.state_admin import AdminMainMenu
from dialog_admin.window_admin import start_admin_menu, visitors, pre_moderate_posts_list, info_window, \
    yandex_weather_window, send_weather, marketing_window
from dialog_user.state_user import UserMainMenu

from filter import AdminFilter

admin_ = Router()
admin_main_menu = Dialog(start_admin_menu(), visitors())
admin_post_manager = Dialog(pre_moderate_posts_list(), info_window())
admin_yandex_weather = Dialog(yandex_weather_window(), send_weather())
admin_marketing = Dialog(marketing_window())

admin_.include_routers(
    admin_main_menu,
    admin_post_manager,
    admin_yandex_weather,
    admin_marketing
)


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK)


async def upload_pic(m: Message):
    id_photo = m.photo[-1].file_id
    await m.answer('ID на сервере Telegram:')
    await m.answer(id_photo)


async def register_admin_handlers():
    admin_.message.filter(AdminFilter())
    admin_.message.register(start, CommandStart())
    admin_.message.register(upload_pic, F.photo, AdminMainMenu.start)
