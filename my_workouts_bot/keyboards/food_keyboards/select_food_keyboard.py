from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils import build_keyboard_menu

from keyboards.keyboard_buttons import SelectFoodButtons


select_food_buttons_list = [
    KeyboardButton(SelectFoodButtons.breakfast),
    KeyboardButton(SelectFoodButtons.bite),
    KeyboardButton(SelectFoodButtons.lunch),
    KeyboardButton(SelectFoodButtons.snack),
    KeyboardButton(SelectFoodButtons.dinner),
    KeyboardButton(SelectFoodButtons.before_sleep),
    KeyboardButton(SelectFoodButtons.day),
    KeyboardButton(SelectFoodButtons.back)
]


select_food_keyboard = ReplyKeyboardMarkup(
    [select_food_buttons_list[:6], [select_food_buttons_list[6]], [select_food_buttons_list[7]]],
    resize_keyboard=True
)