from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from utils import build_keyboard_menu
from keyboards.keyboard_buttons import ChoiceTrainButtons
from utils import build_keyboard_menu, public_url


choice_train_button_list = [
    KeyboardButton(
        text=ChoiceTrainButtons.create,
        web_app=WebAppInfo(url=f'{public_url}/add_user_workout'),
    ),
    KeyboardButton(ChoiceTrainButtons.train),
    KeyboardButton(ChoiceTrainButtons.test_train),
    KeyboardButton(ChoiceTrainButtons.user_train),
    KeyboardButton(ChoiceTrainButtons.back)
]


choice_train_keyboard = ReplyKeyboardMarkup(
    [choice_train_button_list[:2], choice_train_button_list[2:4], choice_train_button_list[4:]],
    resize_keyboard=True
)