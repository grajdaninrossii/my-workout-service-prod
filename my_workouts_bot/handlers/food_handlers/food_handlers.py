from telegram import ReplyKeyboardRemove, Update
from telegram.ext import MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from utils import (
    CHOICE_FOOD
)
import service


from utils.navigation import CHOICE_FOOD_KEY, BACK_KEY
from keyboards import main_menu_keyboard, select_food_keyboard
from keyboards.keyboard_buttons import SelectFoodButtons
from filters import get_day_ration_filter, get_one_ration_filter, select_food_filter
from repositories import dish_repo


async def select_food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOICE_FOOD,
        parse_mode=ParseMode.HTML,
        reply_markup=select_food_keyboard
    )
    return CHOICE_FOOD_KEY


async def get_day_ration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    rezult_text = await service.get_day_ration(update.message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=rezult_text,
        parse_mode=ParseMode.HTML,
        reply_markup=select_food_keyboard
    )
    return CHOICE_FOOD_KEY


async def get_one_ration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    rezult_text = await service.get_one_ration(
        user_id=update.message.from_user.id,
        str_meal=update.message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=rezult_text,
        parse_mode=ParseMode.HTML,
        reply_markup=select_food_keyboard
    )
    return CHOICE_FOOD_KEY


get_day_ration_handler = MessageHandler(get_day_ration_filter, get_day_ration)
get_one_ration_handler = MessageHandler(get_one_ration_filter, get_one_ration)
select_food_handler = MessageHandler(select_food_filter, select_food)