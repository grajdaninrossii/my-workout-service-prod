from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu
from keyboards.keyboard_buttons import SelectFeelingButtons

select_feeling_button_list = [
    KeyboardButton(SelectFeelingButtons.bad),
    KeyboardButton(SelectFeelingButtons.okey),
    KeyboardButton(SelectFeelingButtons.excellent),
    KeyboardButton(SelectFeelingButtons.back)
]

select_feeling_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(select_feeling_button_list, n_cols=2),
    resize_keyboard=True
)