from telegram import ReplyKeyboardRemove, Update
from telegram.ext import MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from utils import (
    ABOUT_BOT,
    ABOUT_BOT_SKILLS,
    FIRST_ENTER_DATA,
    QUESTION_GENDER
)

from utils.navigation import BOT_INFO_KEY, BEGINNING_QUIZ_KEY
from filters import bot_info_filter, bot_skills_filter, beginning_quiz_filter
from keyboards import gender_choice_keyboard


async def get_bot_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ABOUT_BOT,
        parse_mode=ParseMode.HTML
    )
    return BOT_INFO_KEY


async def get_bot_skills_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ABOUT_BOT_SKILLS,
        parse_mode=ParseMode.HTML
    )
    return BOT_INFO_KEY


async def go_2_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{FIRST_ENTER_DATA}{QUESTION_GENDER}',
        reply_markup=gender_choice_keyboard
    )
    return BEGINNING_QUIZ_KEY


get_bot_info_handler = MessageHandler(bot_info_filter, get_bot_info)
get_bot_skills_info_handler = MessageHandler(bot_skills_filter, get_bot_skills_info)
go_2_quiz_handler = MessageHandler(beginning_quiz_filter, go_2_quiz)