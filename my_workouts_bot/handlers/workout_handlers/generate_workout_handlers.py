from config.logger import logging
from telegram import ReplyKeyboardRemove, Update, InputMediaAnimation, InputFile
from telegram.ext import MessageHandler, ContextTypes #, filters
from telegram.constants import ParseMode
from keyboards.keyboard_buttons import ActionInTrainButtons, TypeTrainButtons, ChoiceTrainButtons
from models import Exercise, User
import aiofiles

from utils.navigation import (
    GENERATE_TRAIN_KEY,
    BACK_KEY,
    TYPE_TRAIN_KEY,
    GENERATE_TRAIN_KEY,
    GEN_EX_KEY,
    END_GENERATION_TRAIN_KEY
)

from utils import (
    CHOICE_TRAIN,
    CHOICE_ACTION_TRAIN,
    FAST_TRAIN,
    STANDART_TRAIN,
    STRATCHING,
    WARNING_TEST_TRAIN,
    CHOICE_FEELING,
    STATIC_TRAIN_EXERCISE_DESCRIPTION,
    STANDART_TRAIN_DESCRIPTION,
    EMOM_EXERCISE_DESCRIPTION,
    CROSSFIT_DESCRIPTION,
    WARNING_MANY_WORKOUTS_TODAY,
    VIEW_USER_RATE,
    ADD_USER_RATE,
    USER_WORKOUT,
    WARNING_USER_TRAIN
)

from keyboards import (
    type_train_keyboard,
    choice_train_keyboard,
    select_feeling_keyboard,
    action_in_train_keyboard,
    train_review_keyboard,
    action_in_user_train_keyboards
)

from filters import (
    generate_train_filter,
    select_feeling_filter,
    back_filter,
    type_train_filter,
    next_action_in_train_filters,
    train_review_filter,
    user_train_filter
)
from utils import MaxValueTrainError
import service


async def select_train(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data['feeling'] = update.message.text # сохраняем выбранное самочуствие пользователя
    if context.user_data.get("type_train", None) is not None:
        state: str = await generate_train(update, context)
        return state
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOICE_TRAIN,
        parse_mode=ParseMode.HTML,
        reply_markup=type_train_keyboard
    )
    return GENERATE_TRAIN_KEY


async def select_feeling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    # выбираем тип пользователской тренировки, если данный тип задан
    user_message: str = update.message.text
    if update.message.text == ChoiceTrainButtons.user_train:
        # Нужна проверка на наличие пользовательской тренировки!!!!!!!!!!!!
        rezult: bool = await service.is_exist_user_workouts(update.message.from_user.id)
        if rezult:
            context.user_data['type_train'] = user_message
            await send_choice_feeling_msg(update, context)
            return TYPE_TRAIN_KEY
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=WARNING_USER_TRAIN
        )
    elif not await service.is_good_workout(update.message.from_user.id):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=WARNING_MANY_WORKOUTS_TODAY,
            parse_mode=ParseMode.HTML,
        )
    elif await service.has_exam_train(update.message.from_user.id):
        await send_choice_feeling_msg(update, context)
        return TYPE_TRAIN_KEY
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=WARNING_TEST_TRAIN
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOICE_ACTION_TRAIN,
        parse_mode=ParseMode.HTML,
        reply_markup=choice_train_keyboard
    )
    return BACK_KEY


async def send_choice_feeling_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOICE_FEELING,
        parse_mode=ParseMode.HTML,
        reply_markup=select_feeling_keyboard
    )


# Сохранение данных о тренировке и переход к постепенному выводу упражнений
async def generate_train(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if not await service.is_good_workout(update.message.from_user.id):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=WARNING_MANY_WORKOUTS_TODAY,
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=CHOICE_ACTION_TRAIN,
            parse_mode=ParseMode.HTML,
            reply_markup=choice_train_keyboard
        )
        return BACK_KEY
    user_message: str = update.message.text
    if context.user_data.get('type_train', None) is None:
        match user_message:
            case TypeTrainButtons.fast:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=FAST_TRAIN
            )
            case TypeTrainButtons.standart:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=STANDART_TRAIN
                )
            case TypeTrainButtons.stretching:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=STRATCHING
                )
        context.user_data['type_train'] = user_message
    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=USER_WORKOUT
                )
    context.user_data['current_exercise_number'] = 0 # начало тренировки
    await generate_exercise(update, context)
    return GEN_EX_KEY


async def generate_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    # 10 - кол-во упражнений разминки. По-хорошему, нужно вынести в соответствующий запрос подсчёта
    if update.message.text == ActionInTrainButtons.without_warmup and context.user_data['current_exercise_number'] < 10:
        context.user_data['current_exercise_number'] += 10 - context.user_data['current_exercise_number']

    current_user: User = await service.get_one_user(update.message.from_user.id)
    # Если есть еще упражнения в тренирвоке
    exercise, context.user_data['template_train'], count, user_workout_exercise = await service.generate_exercise(
        user=current_user,
        user_feeling=context.user_data['feeling'],
        type_train=context.user_data['type_train'],
        current_exercise_number=context.user_data['current_exercise_number'],
        template_train=context.user_data.get('template_train', None),
        last_exercise_id=context.user_data.get('last_exercise_id', None)
    )
    if exercise is not None:
        if exercise.type_exercise_id != 5:
            context.user_data['last_exercise_id'] = exercise.id
        context.user_data['current_exercise_number'] += 1
        text_count = f"\n<b>Рекомендуемое кол-во повторений в подходе: {count}</b>"
        try:
            async with aiofiles.open(f"./static{exercise.image_exercise_url}", 'rb') as fl:
                media = InputFile(await fl.read(), filename=None)
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=media
                )
        except Exception as e:
            logging.debug(f'Такого имени файла похоже что нет {str(e)}')
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Видео находится в разработке'
                )
        text_train = ''
        if exercise.type_exercise_id not in [4, 5]:
            text_train = STANDART_TRAIN_DESCRIPTION
            match context.user_data['template_train']:
                case 'statics':
                    text_train = STATIC_TRAIN_EXERCISE_DESCRIPTION
                case 'EMOM':
                    text_train = EMOM_EXERCISE_DESCRIPTION
                case 'crossfit':
                    text_train = CROSSFIT_DESCRIPTION
                case None:
                    text_train = ''
        text_approach = ''
        if user_workout_exercise is not None:
            text_approach = f"\n\nКол-во подходов: {user_workout_exercise.approach_count}"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{exercise.ex_name}{text_train}{text_approach}{text_count if count is not None else ''}\n{exercise.technices}",
            parse_mode=ParseMode.HTML,
            reply_markup=action_in_train_keyboard if context.user_data['type_train'] != ChoiceTrainButtons.user_train else action_in_user_train_keyboards
        )
        return GEN_EX_KEY
    # logging.debug(f'до')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ADD_USER_RATE,
        parse_mode=ParseMode.HTML,
        reply_markup=train_review_keyboard
    )
    # logging.debug(f'после')
    return END_GENERATION_TRAIN_KEY


async def add_review_and_save_train_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    # Присвоить рейтинг + сохранить данные о тренировке
    date, rate = await service.save_train_data(
        user_id=update.message.from_user.id,
        type_train=context.user_data['type_train'],
        review=update.message.text, # ПОМЕНЯТЬ ПОТОМ
        user_feeling=context.user_data['feeling'],
    )

    # Удаление данных о тренирвоке
    context.user_data.pop('last_exercise_id', None)
    context.user_data.pop('current_exercise_number', None)
    type_train = context.user_data.pop('type_train', None)
    context.user_data.pop('template_train', None)
    if type_train == ChoiceTrainButtons.user_train:
        # context.user_data.pop('feeling', None)
        state: str = await back_2_generate_train_menu(update, context)
        return state
    # context.user_data.pop('feeling', None)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOICE_TRAIN,
        parse_mode=ParseMode.HTML,
        reply_markup=type_train_keyboard
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{VIEW_USER_RATE}{rate}',
        parse_mode=ParseMode.HTML
    )
    return GENERATE_TRAIN_KEY


# Вернуться назад (Прежде удалить данные в словаре)
async def back_2_generate_train_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data.pop('last_exercise_id', None)
    context.user_data.pop('current_exercise_number', None)
    context.user_data.pop('type_train', None)
    context.user_data.pop('template_train', None)
    context.user_data.pop('feeling', None)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOICE_ACTION_TRAIN,
        parse_mode=ParseMode.HTML,
        reply_markup=choice_train_keyboard
    )
    return BACK_KEY


select_feeling_handler = MessageHandler(select_feeling_filter | user_train_filter, select_feeling)
select_train_handler = MessageHandler(type_train_filter, select_train)
generate_train_handler = MessageHandler(generate_train_filter, generate_train)
generate_exercise_handler = MessageHandler(next_action_in_train_filters, generate_exercise)
add_review_handler = MessageHandler(train_review_filter, add_review_and_save_train_info)

back_2_generate_train_menu_handler = MessageHandler(back_filter, back_2_generate_train_menu)