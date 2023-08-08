from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu
from keyboards.keyboard_buttons import BotInfoButtons


bot_info_buttons_list = [
    KeyboardButton(BotInfoButtons.more_bot_info),
    KeyboardButton(BotInfoButtons.bot_skills_info),
    KeyboardButton(BotInfoButtons.beginning_quiz)
]


reply_markup_about_bot_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(bot_info_buttons_list, n_cols=1),
    resize_keyboard=True
)