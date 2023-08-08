import asyncio
from filters import all_message_filter, back_filter
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from utils import BAD_ENTER, MAIN_MENU, CHOICE_ACTION_TRAIN, CHOICE_FEELING, CHOICE_TRAIN
from utils.navigation import MAIN_MENU_KEY, CHOICE_TRAIN_KEY, TYPE_TRAIN_KEY, GENERATE_TRAIN_KEY
from utils import loop
from keyboards import main_menu_keyboard, choice_train_keyboard
from config.logger import logging
from typing import Callable


async def get_encorrect_msg(state: str) -> Callable:
    async def send_error_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=BAD_ENTER, # + update.message.text,
                parse_mode=ParseMode.HTML
            )
        text = ''
        reply_keyboard = main_menu_keyboard
        if state is None:
            return state
        elif state == MAIN_MENU_KEY:
            text = MAIN_MENU
        elif state == CHOICE_TRAIN_KEY:
            text = CHOICE_ACTION_TRAIN
        elif state is TYPE_TRAIN_KEY:
            text = CHOICE_FEELING
        elif state is GENERATE_TRAIN_KEY:
            text = CHOICE_TRAIN
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            # reply_markup=reply_keyboard
        )
        return state
    return send_error_msg


encorrect_msg_main_handler = MessageHandler(all_message_filter, loop.run_until_complete(get_encorrect_msg(MAIN_MENU_KEY)))
encorrect_msg_choice_train_handler = MessageHandler(all_message_filter, loop.run_until_complete(get_encorrect_msg(CHOICE_TRAIN_KEY)))
encorrect_msg_choice_feeling_handler = MessageHandler(all_message_filter & ~back_filter, loop.run_until_complete(get_encorrect_msg(TYPE_TRAIN_KEY)))
encorrect_msg_choice_type_train_handler = MessageHandler(all_message_filter & ~back_filter, loop.run_until_complete(get_encorrect_msg(GENERATE_TRAIN_KEY)))
encorrect_msg_handler = MessageHandler(all_message_filter & ~back_filter, loop.run_until_complete(get_encorrect_msg(None)))
