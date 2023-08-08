from telegram import ReplyKeyboardRemove, Update
from telegram.ext import MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode
from config.logger import logging
import json
# from service.workout_service import add_test_exercise

from utils.navigation import (
    CHOICE_TRAIN_KEY,
)


from utils import (
    CHOICE_ACTION_TRAIN,
    ADDED_USER_WORKOUT,
    ADD_USER_WORKOUT_ERROR,
    ADD_USER_WORKOUT_NULL_ERROR
)

from keyboards import choice_train_keyboard, main_menu_keyboard, go_2_test_train_keyboard
import service

exam_train_ex_id_list = [1, 22, 2, 14, 4]


async def save_user_workout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    data = json.loads(update.effective_message.web_app_data.data)
    rezult = await service.save_user_workout(data, update.message.from_user.id)
    if rezult:
        await update.message.reply_html(
            text=ADDED_USER_WORKOUT,
            reply_markup=choice_train_keyboard,
        )
    else:
        await update.message.reply_html(
            text=ADD_USER_WORKOUT_NULL_ERROR,
            reply_markup=choice_train_keyboard,
        )
    await update.message.reply_html(
        text=CHOICE_ACTION_TRAIN,
    )
    return CHOICE_TRAIN_KEY


save_user_workout_handler = MessageHandler(filters.StatusUpdate.WEB_APP_DATA, save_user_workout)