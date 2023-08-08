from telegram import KeyboardButton, ReplyKeyboardMarkup
from keyboards.keyboard_buttons import Go2TestTrainButtons
from utils import build_keyboard_menu


go_2_test_train_button_list = [
    KeyboardButton(Go2TestTrainButtons.yes),
    KeyboardButton(Go2TestTrainButtons.no),
]

go_2_test_train_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(go_2_test_train_button_list, n_cols=1),
    resize_keyboard=True
)