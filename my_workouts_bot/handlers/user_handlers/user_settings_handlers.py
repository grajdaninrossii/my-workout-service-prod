from telegram import ReplyKeyboardRemove, Update
from telegram.ext import MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode
from utils import loop

from utils import (
    QUESTION_GENDER,
    QUESTION_AGE,
    QUESTION_HEIGHT,
    QUESTION_WEIGHT,
    QUESTION_GOAL,
    BAD_ENTER_USER_DATA,
    USER_AGREEMENT_ENTER_QUESTION,
    END_BEGINNING_QUIZ,
    MAIN_MENU,
    POLICY_FOR_DEVELOPMENT,
    MENU_SETTING,
    MENU_USER_SETTING,
    SUPPORT
)

from utils.navigation import (
    SECOND_QUESTION_KEY,
    THIRD_QUESTION_KEY,
    FOURTH_QUESTION_KEY,
    FIFTH_QUESTION_KEY,
    POLICY_KEY,
    MAIN_MENU_KEY,
    SET_USER_DATA_KEY,
    CHOICE_SETTINGS_KEY,
    SET_GENDER_KEY,
    SET_AGE_KEY,
    SET_HEIGHT_KEY,
    SET_WEIGHT_KEY,
    SET_GOAL_KEY,
    BEGINNING_QUIZ_KEY
)

from filters import (
    set_gender_filter,
    fset_goal_filter,
    policy_agree_filter,
    set_data_filter,
    settings_filter,
    support_filter,
    user_settings_filter,
    choice_settings_filter,
    back_filter,
    get_user_data_filter
)

import service

from keyboards import gender_choice_keyboard, policy_agree_keyboard, goal_choice_keyboard, main_menu_keyboard, user_settings_keyboard, settings_keyboard
from keyboards.keyboard_buttons import UserSettingsButtons
from typing import Callable
from config.logger import logging

async def set_user_gender(state: str) -> Callable:
    async def set_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await service.set_user_gender(update.message.from_user.id, update.message.text)

        bot_answer = MENU_USER_SETTING
        keyboard = user_settings_keyboard
        new_state = SET_USER_DATA_KEY
        if state == BEGINNING_QUIZ_KEY:
            bot_answer = QUESTION_AGE
            new_state=SECOND_QUESTION_KEY
            keyboard = ReplyKeyboardRemove()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Данные сохранены {bot_answer}',
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
        return new_state
    return set_gender


async def set_user_age(state: str) -> Callable:
    async def set_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        bot_answer = await service.set_user_age(update.message.from_user.id, update.message.from_user.username, update.message.text)
        if 'Данные сохранены' in bot_answer:
            text = f'{bot_answer} {MENU_USER_SETTING}'
            keyboard = user_settings_keyboard
            new_state = SET_USER_DATA_KEY
            if state == SECOND_QUESTION_KEY:
                text = f'{bot_answer} {QUESTION_HEIGHT}'
                keyboard = ReplyKeyboardRemove()
                new_state = THIRD_QUESTION_KEY
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )
            return new_state
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'{bot_answer} {BAD_ENTER_USER_DATA}'
            )
        return state
    return set_age


async def set_user_height(state: str) -> Callable:
    async def set_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        bot_answer = await service.set_user_height(update.message.from_user.id, update.message.text)
        if 'Данные сохранены' in bot_answer:
            text = f'{bot_answer} {MENU_USER_SETTING}'
            keyboard = user_settings_keyboard
            new_state = SET_USER_DATA_KEY
            if state == THIRD_QUESTION_KEY:
                text = f'{bot_answer} {QUESTION_WEIGHT}'
                keyboard = ReplyKeyboardRemove()
                new_state = FOURTH_QUESTION_KEY
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
                )
            return new_state
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'{bot_answer} {BAD_ENTER_USER_DATA}',
                parse_mode=ParseMode.HTML
                )
        return state
    return set_height


async def set_user_weight(state: str) -> Callable:
    async def set_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        bot_answer = await service.set_user_weight(update.message.from_user.id, update.message.text)
        if 'Данные сохранены' in bot_answer:
            text = f'{bot_answer} {MENU_USER_SETTING}'
            keyboard = user_settings_keyboard
            new_state = SET_USER_DATA_KEY
            if state == FOURTH_QUESTION_KEY:
                text = f'{bot_answer} {QUESTION_GOAL}'
                keyboard = goal_choice_keyboard
                new_state = FIFTH_QUESTION_KEY
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
                )
            return new_state
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'{bot_answer} {BAD_ENTER_USER_DATA}',
                parse_mode=ParseMode.HTML,
                # reply_markup=goal_choice_keyboard
                )
        return state
    return set_weight


async def set_user_goal(state: str) -> str:
    async def set_goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        await service.set_user_goal(update.message.from_user.id, update.message.text)
        if state == FIFTH_QUESTION_KEY:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Данные сохранены! {USER_AGREEMENT_ENTER_QUESTION}',
                parse_mode=ParseMode.HTML,
                # reply_markup=ReplyKeyboardRemove()
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=POLICY_FOR_DEVELOPMENT,
                parse_mode=ParseMode.HTML,
                reply_markup=policy_agree_keyboard
            )
            return POLICY_KEY
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Данные сохранены! {MENU_USER_SETTING}',
            parse_mode=ParseMode.HTML,
            reply_markup=user_settings_keyboard
        )
        return SET_USER_DATA_KEY
    return set_goal


async def set_agree_policy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await service.set_agree_policy(update.message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Данные сохранены! {END_BEGINNING_QUIZ}',
        parse_mode=ParseMode.HTML,
        # reply_markup=main_menu_keyboard
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MAIN_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard
    )
    return MAIN_MENU_KEY


async def get_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    bot_answer = await service.get_user_data(update.message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_answer,
        parse_mode=ParseMode.HTML,
    )
    return SET_USER_DATA_KEY


async def get_user_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MENU_USER_SETTING,
        parse_mode=ParseMode.HTML,
        reply_markup=user_settings_keyboard
    )
    return SET_USER_DATA_KEY


# Выбор характеристики для изменения
async def choice_user_setting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

    bot_answer = QUESTION_GOAL
    keyboard = goal_choice_keyboard
    new_state = SET_GOAL_KEY
    match update.message.text:
        case UserSettingsButtons.gender:
            bot_answer = QUESTION_GENDER
            keyboard = gender_choice_keyboard
            new_state = SET_GENDER_KEY
        case UserSettingsButtons.age:
            bot_answer = QUESTION_AGE
            keyboard = ReplyKeyboardRemove()
            new_state = SET_AGE_KEY
        case UserSettingsButtons.height:
            bot_answer = QUESTION_HEIGHT
            keyboard = ReplyKeyboardRemove()
            new_state = SET_HEIGHT_KEY
        case UserSettingsButtons.weight:
            bot_answer = QUESTION_WEIGHT
            keyboard = ReplyKeyboardRemove()
            new_state = SET_WEIGHT_KEY
    logging.debug(f'Что с тобой не так? {bot_answer, new_state}')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_answer,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    return new_state


async def get_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MENU_SETTING,
        parse_mode=ParseMode.HTML,
        reply_markup=settings_keyboard
    )
    return CHOICE_SETTINGS_KEY


async def get_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=SUPPORT,
        parse_mode=ParseMode.HTML
    )
    return CHOICE_SETTINGS_KEY


async def back_to_setting_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MENU_SETTING,
        parse_mode=ParseMode.HTML,
        reply_markup=settings_keyboard
    )
    return CHOICE_SETTINGS_KEY


# Прохождение первоначального тестирования
set_gender_quiz_handler = MessageHandler(set_gender_filter, loop.run_until_complete(set_user_gender(BEGINNING_QUIZ_KEY)))
set_age_quiz_handler = MessageHandler(set_data_filter, loop.run_until_complete(set_user_age(SECOND_QUESTION_KEY)))
set_height_quiz_handler = MessageHandler(set_data_filter, loop.run_until_complete(set_user_height(THIRD_QUESTION_KEY)))
set_weight_quiz_handler = MessageHandler(set_data_filter, loop.run_until_complete(set_user_weight(FOURTH_QUESTION_KEY)))
set_goal_quiz_handler = MessageHandler(fset_goal_filter, loop.run_until_complete(set_user_goal(FIFTH_QUESTION_KEY)))
set_agree_policy_quiz_handler = MessageHandler(policy_agree_filter, set_agree_policy)

# Настройки
settings_handler = MessageHandler(settings_filter, get_settings)
support_handler = MessageHandler(support_filter, get_support)
user_settings_handler = MessageHandler(user_settings_filter, get_user_settings)

choice_user_setting_handler = MessageHandler(choice_settings_filter, choice_user_setting)
back_to_setting_menu_handler = MessageHandler(back_filter & ~filters.COMMAND, back_to_setting_menu)

# Изменение данных пользователя
set_gender_handler = MessageHandler(set_gender_filter, loop.run_until_complete(set_user_gender(SET_GENDER_KEY)))
set_age_handler = MessageHandler(set_data_filter, loop.run_until_complete(set_user_age(SET_AGE_KEY)))
set_height_handler = MessageHandler(set_data_filter, loop.run_until_complete(set_user_height(SET_HEIGHT_KEY)))
set_weight_handler = MessageHandler(set_data_filter, loop.run_until_complete(set_user_weight(SET_WEIGHT_KEY)))
set_goal_handler = MessageHandler(fset_goal_filter, loop.run_until_complete(set_user_goal(SET_GOAL_KEY)))

# Получение данных пользователя
get_user_data_handler = MessageHandler(get_user_data_filter, get_user_data)