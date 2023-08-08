from keyboards.keyboard_buttons import PolicyAgreeButtonsButtons

from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from utils import build_keyboard_menu, public_url


button_list_answer_five_quiz_goal = [
    KeyboardButton(PolicyAgreeButtonsButtons.agree),
    KeyboardButton(
        text=PolicyAgreeButtonsButtons.document,
        web_app=WebAppInfo(url=f'{public_url}/policy'),
    )
]


policy_agree_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(button_list_answer_five_quiz_goal, n_cols=1),
    resize_keyboard=True
)