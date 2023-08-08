from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu
from keyboards.keyboard_buttons import TrainReviewButtons

train_review_button_list = [
    KeyboardButton(TrainReviewButtons.hard),
    KeyboardButton(TrainReviewButtons.easy),
    KeyboardButton(TrainReviewButtons.optim)
]

train_review_keyboard = ReplyKeyboardMarkup(
    build_keyboard_menu(train_review_button_list, n_cols=1),
    resize_keyboard=True
)