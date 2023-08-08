from telegram import KeyboardButton, ReplyKeyboardMarkup

from keyboards.keyboard_buttons import SettingsButtons
from utils import build_keyboard_menu

settings_buttons_list = [
    KeyboardButton(SettingsButtons.profile),
    KeyboardButton(SettingsButtons.support),
    KeyboardButton(SettingsButtons.back)
]


settings_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(settings_buttons_list, n_cols=1),
    resize_keyboard=True
)