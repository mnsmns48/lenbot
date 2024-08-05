from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog

from dialog_admin.callback_admin import upload_pic
from dialog_admin.state_admin import AdminMainMenu, LoadImage
from dialog_admin.window_admin import start_admin_menu, visitors, pre_moderate_posts_list, info_window, \
    yandex_weather_window, send_weather, marketing_window, send_image

from filter import AdminFilter

admin_ = Router()
admin_main_menu = Dialog(start_admin_menu(), visitors())
admin_post_manager = Dialog(pre_moderate_posts_list(), info_window())
admin_yandex_weather = Dialog(yandex_weather_window(), send_weather())
admin_marketing = Dialog(marketing_window())
admin_send_image = Dialog(send_image())

admin_.include_routers(
    admin_main_menu,
    admin_post_manager,
    admin_yandex_weather,
    admin_marketing,
    admin_send_image
)


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK)


async def register_admin_handlers():
    admin_.message.filter(AdminFilter())
    admin_.message.register(start, CommandStart())
    admin_.message.register(upload_pic, F.photo, LoadImage.get_image)
