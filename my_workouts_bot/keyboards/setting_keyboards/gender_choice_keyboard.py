from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu

from keyboards.keyboard_buttons import GenderChoiceButtons


bot_question_buttons_list = [
    KeyboardButton(GenderChoiceButtons.male),
    KeyboardButton(GenderChoiceButtons.female)
]


gender_choice_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(bot_question_buttons_list, n_cols=1),
    resize_keyboard=True
)

