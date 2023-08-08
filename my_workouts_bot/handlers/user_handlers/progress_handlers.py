from fileinput import FileInput
from io import BytesIO
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from utils import (
    VIEW_GRAPHIC,
    VIEW_USER_RATE,
    VIEW_GRAPHIC_ERROR
)

from utils.navigation import (
    CHOICE_PROGRESS_KEY
)

from filters import (
    get_progress_filter,
    get_progress_graphic_filter
)

import service
from keyboards import progress_keyboard
from config.logger import logging


async def get_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_rate: int = await service.get_user_rate(update.message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{VIEW_USER_RATE}{user_rate}',
        parse_mode=ParseMode.HTML,
        reply_markup=progress_keyboard
    )
    return CHOICE_PROGRESS_KEY


async def get_progress_graphic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    plt_fig = await service.get_plot_user_train(update.message.from_user.id)
    if plt_fig is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=VIEW_GRAPHIC_ERROR,
            parse_mode=ParseMode.HTML
        )
        return CHOICE_PROGRESS_KEY

    plot_file = BytesIO()
    plt_fig.savefig(plot_file, format='png')
    plot_file.seek(0)

    logging.debug(f"test img {plot_file}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=VIEW_GRAPHIC,
        parse_mode=ParseMode.HTML
    )
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=plot_file,
        parse_mode=ParseMode.HTML
    )
    return CHOICE_PROGRESS_KEY


progress_handler = MessageHandler(get_progress_filter, get_progress)
progress_graphic_handler = MessageHandler(get_progress_graphic_filter, get_progress_graphic)