from aiogram_dialog import Dialog

from dialog_premoderate.windows_premod import pre_moderate_posts, info_window, start_admin_menu, yandex_weather_window, \
    send_weather, marketing_window, visitors

admin_main_menu = Dialog(start_admin_menu(), visitors())
admin_post_manager = Dialog(pre_moderate_posts(), info_window())
admin_yandex_weather = Dialog(yandex_weather_window(), send_weather())
admin_marketing = Dialog(marketing_window())