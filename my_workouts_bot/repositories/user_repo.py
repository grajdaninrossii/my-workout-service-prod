from sqlalchemy import func, select, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi_asyncalchemy.models import *

from models import User
from models import CalendarStatistics
from datetime import datetime, timedelta, date
from config.logger import logging


async def get_all_users(session: AsyncSession) -> list[User]:
    rezult = await session.execute(select(User))
    return rezult.scalars().all()


async def get_one_user(session: AsyncSession, user_id: int) -> User:
    rezult = await session.get(User, user_id)
    return rezult


async def user_is_exist(session: AsyncSession, user_id: int) -> bool:
    rezult = await session.execute(select(exists(User).where(User.id==user_id)))
    return rezult.scalar()


def add_user(session: AsyncSession, user_id, username: int, age: int = None) -> User:
    user: User = User(user_id, username, age)
    session.add(user)
    return user


async def update_age_user(session: AsyncSession, user_id: int, parameter: 'str', new_value: int) -> None:
    await session.execute(update(User)
        .where(User.id == user_id)
        .values(age=new_value)
        .execution_options(synchronize_session="evaluate")
    )


async def save_train(session: AsyncSession, user_id: int, type_train_id: int, review_id: int, feeling_id: int) -> CalendarStatistics:
    train_date = datetime.now()
    story_train_date = CalendarStatistics(user_id, type_train_id, review_id, feeling_id, train_date)
    logging.debug(f'Смотри объект {story_train_date}')
    session.add(story_train_date)
    return story_train_date


async def count_train_today(session: AsyncSession, user_id: int) -> int:
    last_train_date = datetime.now() - timedelta(days=1)
    count_workouts = await session.execute(select(func.count(CalendarStatistics.id))
        .where(CalendarStatistics.user_id == user_id, CalendarStatistics.training_date > last_train_date)
    )
    return count_workouts.one()[0]


async def get_user_rate(session: AsyncSession, user_id: int) -> int:
    rezult = await session.execute(select(User.rate).where(User.id == user_id))
    return rezult.one()[0]


async def get_user_train_month_calendar(session: AsyncSession, user_id: int) -> list[CalendarStatistics]:
    current_date = date.today()
    first_day_of_month = current_date - timedelta(days=current_date.day)
    rezult = await session.execute(select(CalendarStatistics)
        .where(CalendarStatistics.user_id == user_id, CalendarStatistics.training_date > first_day_of_month))
    return rezult.scalars().all()

# async def get_user_gender(session: AsyncSession, user_id: int) -> list:
#     rezult = await session.execute(select(User).join(User.gender))
#     return rezult.scalars().all()
    # print(rezult)

# async def get_biggest_cities(session: AsyncSession) -> list[City]:
#     result = await session.execute(select(City).order_by(City.population.desc()).limit(20))
#     return result.scalars().all()


# def add_city(session: AsyncSession, name: str, population: int):
#     new_city = City(name=name, population=population)
#     session.add(new_city)
#     return new_city