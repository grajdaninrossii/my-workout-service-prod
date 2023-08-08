from telegram import ReplyKeyboardRemove, Update
from telegram.ext import MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode
from config.logger import logging
# from service.workout_service import add_test_exercise

from utils.navigation import (
    PUSH_UP_TEST_KEY,
    RUNNING_3KM_TEST_KEY,
    SQUAT_TEST_KEY,
    PRESS_TEST_KEY,
    PULL_UP_TEST_KEY,
    BACK_KEY,
    CHOICE_TRAIN_KEY,
    MAIN_MENU_KEY,
    GO_2_PUSH_UP_TEST_KEY
)


from utils import (
    BAD_ENTER_USER_DATA,
    CHOICE_ACTION_TRAIN,
    WARNING_TEST_TRAIN,
    BEGIN_TEST_TRAIN,
    PUSH_UP_TEST,
    RUNNING_3KM_TEST,
    SQUAT_TEST,
    PRESS_TEST,
    PULL_UP_TEST,
    COMPLETE_TEST_TRAIN,
    MAIN_MENU
)

from keyboards import choice_train_keyboard, main_menu_keyboard, go_2_test_train_keyboard
from filters import set_data_with_back_filter, back_filter, test_train_filter, go_2_test_train_filter
import service

exam_train_ex_id_list = [1, 22, 2, 14, 4]


async def select_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOICE_ACTION_TRAIN,
        parse_mode=ParseMode.HTML,
        reply_markup=choice_train_keyboard
    )
    return CHOICE_TRAIN_KEY


async def begin_test_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=BEGIN_TEST_TRAIN,
        parse_mode=ParseMode.HTML,
        reply_markup=go_2_test_train_keyboard # добавить клаву
    )
    # logging.debug("TESTSTSTT" + str(context.user_data))
    return GO_2_PUSH_UP_TEST_KEY


async def go_2_test_train(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=PUSH_UP_TEST,
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )
    return PUSH_UP_TEST_KEY

async def set_push_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    bot_answer = await service.add_test_exercise(update.message.from_user.id, exam_train_ex_id_list[0], update.message.text)
    if 'Данные сохранены' in bot_answer:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {RUNNING_3KM_TEST}',
            reply_markup=ReplyKeyboardRemove()
        )
        return RUNNING_3KM_TEST_KEY
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {BAD_ENTER_USER_DATA}'
        )
    return PUSH_UP_TEST_KEY


async def set_running_3km(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    bot_answer = await service.add_test_exercise(update.message.from_user.id, exam_train_ex_id_list[1], update.message.text)
    if 'Данные сохранены' in bot_answer:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {SQUAT_TEST}',
            reply_markup=ReplyKeyboardRemove()
        )
        return SQUAT_TEST_KEY
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {BAD_ENTER_USER_DATA}'
        )
    return RUNNING_3KM_TEST_KEY


async def set_squat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    bot_answer = await service.add_test_exercise(update.message.from_user.id, exam_train_ex_id_list[2], update.message.text)
    if 'Данные сохранены' in bot_answer:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {PRESS_TEST}',
            reply_markup=ReplyKeyboardRemove()
        )
        return PRESS_TEST_KEY
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {BAD_ENTER_USER_DATA}'
        )
    return SQUAT_TEST_KEY


async def set_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    bot_answer = await service.add_test_exercise(update.message.from_user.id, exam_train_ex_id_list[3], update.message.text)
    if 'Данные сохранены' in bot_answer:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {PULL_UP_TEST}',
            reply_markup=ReplyKeyboardRemove()
        )
        return PULL_UP_TEST_KEY
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {BAD_ENTER_USER_DATA}'
        )
    return PRESS_TEST_KEY


async def set_pull_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    bot_answer = await service.add_test_exercise(update.message.from_user.id, exam_train_ex_id_list[4], update.message.text)
    if 'Данные сохранены' in bot_answer:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {COMPLETE_TEST_TRAIN}',
            reply_markup=ReplyKeyboardRemove()
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=CHOICE_ACTION_TRAIN,
            parse_mode=ParseMode.HTML,
            reply_markup=choice_train_keyboard
        )
        return   CHOICE_TRAIN_KEY
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{bot_answer} {BAD_ENTER_USER_DATA}'
        )
    return PULL_UP_TEST_KEY


async def back_to_train_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await select_action(update, context)


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MAIN_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard
    )
    return MAIN_MENU_KEY


back_2_train_menu_handler = MessageHandler(back_filter & ~filters.COMMAND, back_to_train_menu)
back_2_main_menu_handler = MessageHandler(back_filter & ~filters.COMMAND, back_to_main_menu)

set_push_up_handler = MessageHandler(set_data_with_back_filter, set_push_up)
set_running_3km_handler = MessageHandler(set_data_with_back_filter, set_running_3km)
set_squat_handler = MessageHandler(set_data_with_back_filter, set_squat)
set_press_handler = MessageHandler(set_data_with_back_filter, set_press)
set_pull_up_handler = MessageHandler(set_data_with_back_filter, set_pull_up)
# complete_test_workout_handler = MessageHandler(set_data_with_back_filter, complete_test_workout)

begin_test_handler = MessageHandler(test_train_filter, begin_test_workout)
go_2_test_train_handler = MessageHandler(go_2_test_train_filter, go_2_test_train)

select_action_handler = MessageHandler(filters.Regex(f'Тренировки 🏓'), select_action)