from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu
from keyboards.keyboard_buttons import TypeTrainButtons

type_train_button_list = [
    KeyboardButton(TypeTrainButtons.fast),
    KeyboardButton(TypeTrainButtons.standart),
    KeyboardButton(TypeTrainButtons.stretching),
    KeyboardButton(TypeTrainButtons.back)
]

type_train_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(type_train_button_list, n_cols=2),
    resize_keyboard=True
)