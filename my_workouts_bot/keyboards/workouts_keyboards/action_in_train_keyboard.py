from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu
from keyboards.keyboard_buttons import ActionInTrainButtons


action_in_train_button_list = [
    KeyboardButton(ActionInTrainButtons.without_warmup),
    KeyboardButton(ActionInTrainButtons.next_exercise),
    KeyboardButton(ActionInTrainButtons.back)
]


action_in_train_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(action_in_train_button_list, n_cols=2),
    resize_keyboard=True
)

action_in_user_train_keyboards = ReplyKeyboardMarkup(
    build_keyboard_menu([action_in_train_button_list[1], action_in_train_button_list[2]], n_cols=1),
    resize_keyboard=True
)