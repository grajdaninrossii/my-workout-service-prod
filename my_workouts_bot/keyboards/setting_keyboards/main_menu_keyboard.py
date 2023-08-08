from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu

from keyboards.keyboard_buttons import MainMenuButtons


button_list_answer_five_quiz_goal = [
    KeyboardButton(MainMenuButtons.sport),
    KeyboardButton(MainMenuButtons.food),
    KeyboardButton(MainMenuButtons.settings),
    KeyboardButton(MainMenuButtons.progress)
]


main_menu_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(button_list_answer_five_quiz_goal, n_cols=2),
    resize_keyboard=True
)