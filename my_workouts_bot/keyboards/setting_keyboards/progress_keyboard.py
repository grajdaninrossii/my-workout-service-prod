from telegram import KeyboardButton, ReplyKeyboardMarkup

from keyboards.keyboard_buttons import ProgressButtons
from utils import build_keyboard_menu

progress_buttons_list = [
    KeyboardButton(ProgressButtons.graphic),
    KeyboardButton(ProgressButtons.back)
]


progress_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(progress_buttons_list, n_cols=1),
    resize_keyboard=True
)