from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
import aiofiles

from utils import GREETING, POLICY_FOR_DEVELOPMENT
from utils.navigation import BOT_INFO_KEY, MAIN_MENU_KEY, POLICY_KEY
# from messages import GREETING, BOT_IN
from keyboards import reply_markup_about_bot_keyboard, policy_agree_keyboard
# from u import db
import service

# from .beginning_quiz_handlers import db

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiofiles.open('./static/images/test_send_photo.jpg', 'rb') as fl:
        await service.add_useruser_if_is_not_exist(update.message.from_user.id, update.message.from_user.username)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo= await fl.read()
            )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=GREETING,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup_about_bot_keyboard
            )
        # await context.bot.send_message(
        #         chat_id=update.effective_chat.id,
        #         text=POLICY_FOR_DEVELOPMENT,
        #         parse_mode=ParseMode.HTML,
        #         reply_markup=policy_agree_keyboard
        #     )
    return BOT_INFO_KEY
    # return POLICY_KEY


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_message_id = update.message.message_id
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пока",
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup_about_bot_keyboard
        )
    while new_message_id > 1:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=new_message_id)
        except Exception as error:
            print(f'Message_id does not exist: {new_message_id} - {error}')
        new_message_id = new_message_id - 1
    return BOT_INFO_KEY
    # return MAIN_MENU_KEY # Для тестов


start_handler = CommandHandler('start', start) # добавляем команду /start и ее обработчик start
clear_handler = CommandHandler('clear', clear)