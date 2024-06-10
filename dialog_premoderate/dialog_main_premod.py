from aiogram_dialog import Dialog

from dialog_premoderate.windows_premod import pre_moderate_posts, info_window

posts_dialog = Dialog(
    pre_moderate_posts(),
    info_window()
)
