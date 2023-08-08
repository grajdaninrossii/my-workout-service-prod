from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu

from keyboards.keyboard_buttons import GoalChoiceButtons


button_list_answer_five_quiz_goal = [
    KeyboardButton(GoalChoiceButtons.mass),
    KeyboardButton(GoalChoiceButtons.maintenance),
    KeyboardButton(GoalChoiceButtons.flexibility),
    KeyboardButton(GoalChoiceButtons.endurance)
]


goal_choice_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(button_list_answer_five_quiz_goal, n_cols=2),
    resize_keyboard=True
)