import seaborn as sns
from models import async_session
from keyboards.keyboard_buttons import GoalChoiceButtons, GenderChoiceButtons, SelectFeelingButtons, TypeTrainButtons, TrainReviewButtons
from models import User, CalendarStatistics
from repositories import user_repo

from utils import AgeValueError, HeightValueError, WeightValueError
from config.logger import logging
from keyboards.keyboard_buttons import UserSettingsButtons
from datetime import datetime
import locale
# locale.setlocale(locale.LC_TIME, 'ru')
locale.setlocale(locale.LC_ALL,'ru_RU.UTF-8')
sns.set_style("whitegrid")


async def add_useruser_if_is_not_exist(user_id: int, username: str) -> bool:
    async with async_session() as session:
        # Создание/взятие пользователя из бд
        # current_user = await service.get_one_user(session, update.message.from_user.id)
        is_exist = await user_repo.user_is_exist(session, user_id)
        if not is_exist:
            current_user = user_repo.add_user(session, user_id=user_id, username=username)
            await session.commit()
            return True
        return False
    # return True if current_user is not None else False


async def set_user_gender(user_id: int, user_text: str) -> None:
    async with async_session() as session:
        gender_id = 0
        for i, x in enumerate(GenderChoiceButtons, 1):
            if x.value == user_text:
                gender_id = i
                break

        current_user = await user_repo.get_one_user(session, user_id)
        if current_user is None:
            logging.debug("Ошибка входа! Обработать нестандарный вариант поведения.")
        current_user.gender_id = gender_id
        await session.commit()


async def set_user_goal(user_id: int, user_text: str) -> None:
    async with async_session() as session:
        goal_id = 0
        for i, x in enumerate(GoalChoiceButtons, 1):
            if x.value == user_text:
                goal_id = i
                break

        current_user = await user_repo.get_one_user(session, user_id)
        current_user.goal_id = goal_id
        await session.commit()


async def set_agree_policy(user_id: int) -> None:
    async with async_session() as session:
        current_user = await user_repo.get_one_user(session, user_id)
        current_user.is_agree = True
        if current_user.rate is None:
            current_user.rate = 0
        await session.commit()


async def set_user_age(user_id: int, username: str, user_text: str) -> str:
    async with async_session() as session:
        bot_answer: str = ''
        try:
            user_age = int(user_text)
            if user_age not in range(18, 80):
                raise AgeValueError("Возраст задается в диапазоне от 18 до 80 лет!")

            # Создание/взятие пользователя из бд
            current_user: User = await user_repo.get_one_user(session, user_id)
            if current_user is None:
                current_user = user_repo.add_user(session, user_id=user_id, username=username, age=user_age)
            else:
                current_user.age = user_age
            await session.commit()
            bot_answer = f'Данные сохранены!'
        except ValueError:
            bot_answer = f'Некорректные данные!'
        except AgeValueError as error:
            bot_answer = str(error)
    return bot_answer


async def set_user_height(user_id: int, user_text: str) -> str:
    async with async_session() as session:
        bot_answer: str = ''
        try:
            user_height = int(user_text)
            if user_height not in range(140, 220):
                raise HeightValueError("Рост задается в диапазоне от 140 до 220 см!")

            # Создание/взятие пользователя из бд
            current_user: User = await user_repo.get_one_user(session, user_id)
            current_user.height = user_height
            await session.commit()
            bot_answer = f'Данные сохранены!'
        except ValueError:
            bot_answer = f'Некорректные данные!'
        except HeightValueError as error:
            bot_answer = str(error)
    return bot_answer


async def set_user_weight(user_id: int, user_text: str) -> str:
    async with async_session() as session:
        bot_answer: str = ''
        try:
            user_weight = int(user_text)
            if user_weight not in range(40, 130):
                raise WeightValueError("Вес задается в диапазоне от 40 до 130 кг!")

            # Создание/взятие пользователя из бд
            current_user: User = await user_repo.get_one_user(session, user_id)
            current_user.weight = user_weight
            await session.commit()
            bot_answer = f'Данные сохранены!'
        except ValueError:
            bot_answer = f'Некорректные данные!'
        except WeightValueError as error:
            bot_answer = str(error)
    return bot_answer


async def get_one_user(user_id: int) -> User:
    async with async_session() as session:
        current_user: User = await user_repo.get_one_user(session, user_id) # Достаём объект пользователя
    return current_user


# Проверка количества тренировок в последние сутки
async def is_good_workout(user_id: int) -> bool:
    async with async_session() as session:
        rezult: bool = True
        count_train_today: int = await user_repo.count_train_today(session, user_id)
        if count_train_today is not None:
            if count_train_today > 3:
                rezult = False
        return rezult


# Получение данных пользователя
async def get_user_data(user_id: int):
    async with async_session() as session:
        current_user: User = await user_repo.get_one_user(session, user_id) # Достаём объект пользователя
        age_type: str = ''
        match current_user.age % 10:
            case 1:
                age_type = 'год'
            case 2|3|4:
                age_type = 'года'
            case 0|5|6|7|8|9:
                age_type = 'лет'
        rezult: str = (f'Ваши данные 📋: \n'
                  f'Пол {UserSettingsButtons.gender} - {current_user.gender.gender_name}\n'
                  f'Возраст {UserSettingsButtons.age} - {current_user.age} {age_type}\n'
                  f'Рост {UserSettingsButtons.height} - {current_user.height} см\n'
                  f'Вес {UserSettingsButtons.weight} - {current_user.weight} кг\n'
                  f'Цель {UserSettingsButtons.goal} - {current_user.goal.goal_name}\n'
                  )
    return rezult


async def get_user_rate(user_id: int) -> int:
    async with async_session() as session:
        user_rate: int = await user_repo.get_user_rate(session, user_id)
    return user_rate


async def save_train_data(
    user_id: int,
    type_train: str,
    review: int, # ПОМЕНЯТЬ ПОТОМ
    user_feeling: str) -> CalendarStatistics:
    async with async_session() as session:
        user = await user_repo.get_one_user(session, user_id)
        # Получаем id самочуствия
        feeling_id = 1
        match user_feeling:
            case SelectFeelingButtons.bad:
                feeling_id = 3
            case SelectFeelingButtons.okey:
                feeling_id = 2

        type_train_id = 1
        rate_reward: int = 1
        match type_train:
            case TypeTrainButtons.standart:
                type_train_id = 2
                rate_reward = 2
            case TypeTrainButtons.stretching:
                type_train_id = 4

        review_id = 1
        match review:
            case TrainReviewButtons.easy:
                review_id = 2
            case TrainReviewButtons.optim:
                review_id = 3

        calendar_statistics: CalendarStatistics = await user_repo.save_train(session, user.id, type_train_id, review_id, feeling_id) # Достаём объект пользователя
        # session.add(user)
        if user.rate is not None:
            user.rate += rate_reward
        else:
            user.rate = rate_reward
        user_rate = user.rate
        await session.commit()
    return calendar_statistics, user_rate


async def get_plot_user_train(user_id: int):
    async with async_session() as session:
        user: User = await user_repo.get_one_user(session, user_id)
        training_date_month: list[CalendarStatistics] | None = await user_repo.get_user_train_month_calendar(session, user_id)
        if training_date_month == []:
            return None
        dict_train_date: dict = {'x': [], 'y': []}
        last_training_day = training_date_month[0].training_date.day
        count = 0
        for train_date in training_date_month:
            if last_training_day == train_date.training_date.day:
                count += 1
            else:
                dict_train_date['x'].append(last_training_day)
                dict_train_date['y'].append(count)
                last_training_day = train_date.training_date.day
                count = 1
        dict_train_date['x'].append(last_training_day)
        dict_train_date['y'].append(count)

        sns_plot = sns.barplot(data=dict_train_date, x="x", y="y", palette="plasma")
        sns_plot.set_xlabel(f'{datetime.now().strftime("%B")}')
        sns_plot.set_ylabel('Кол-во тренировок')
        sns_plot.set_title('Статистика тренировок в текущем месяце')

    return sns_plot.get_figure()