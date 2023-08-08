from sqlalchemy import func, select, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi_asyncalchemy.models import *

from models import Exercise, ExamWorkout
from models import Muscule, muscule_exercise_groups_table
from models.workout import ExerciseUserWorkout, UserWorkout, ExerciseUserWorkout
from config.logger import logging


async def get_all_exercises(session: AsyncSession) -> list[Exercise]:
    rezult = await session.execute(select(Exercise))
    return rezult.scalars().all()


async def get_one_ex(session: AsyncSession, ex_id: int) -> Exercise:
    rezult = await session.get(Exercise, ex_id)
    return rezult


async def get_one_exam_workout(session: AsyncSession, user_id: int, ex_id) -> ExamWorkout:
    rezult = await session.get(ExamWorkout, (user_id, ex_id))
    return rezult


async def get_all_ex_id_in_exam_workout(session: AsyncSession, user_id: int, type_exam_id: list[int]) -> list[ExamWorkout]:
    rezult = await session.execute(
        select(ExamWorkout.exercise_id, ExamWorkout.values)
        .where(ExamWorkout.user_id == user_id, ExamWorkout.exercise_id.in_(type_exam_id))
        .order_by(ExamWorkout.exercise_id)
    )
    return rezult.all()


async def get_exam_exs_user(session: AsyncSession, user_id) -> list[ExamWorkout]:
    result = await session.execute(
        select(ExamWorkout).where(ExamWorkout.user_id == user_id)
    )
    return result.scalars().all()


async def get_all_exercise_with_where(session: AsyncSession, type_exercise_id: int) -> list[Exercise]:
    result = await session.execute(
        select(Exercise).where(Exercise.type_exercise_id == type_exercise_id).order_by(Exercise.id)
    )
    return result.scalars().all()


async def get_first_exercise_with_2_where(session: AsyncSession, type_exercise_id: int, not_ex_id: int) -> list[Exercise]:
    result = await session.execute(
        select(Exercise)
            .where(Exercise.type_exercise_id == type_exercise_id, Exercise.id != not_ex_id)
            .order_by(func.random())
    )
    return result.scalars().first()


async def get_first_exercise_with_3_where(session: AsyncSession, type_exercise_id: int, not_ex_id: int, muscule_id) -> list[Exercise]:
    result = await session.execute(
        select(Exercise)
            .join(Exercise.muscules)
            .where(Muscule.id == muscule_id, Exercise.type_exercise_id == type_exercise_id, Exercise.id != not_ex_id)
            # .distinct()
            .order_by(func.random())
        )
    return result.scalars().first()


async def get_all_ex_muscules_with_conds(session: AsyncSession, muscule_id: int, type_exercise_id: int) -> list[Exercise]:
    rezult = await session.execute(
        select(Exercise)
            .join(Exercise.muscules)
            .where(Muscule.id == muscule_id, Exercise.type_exercise_id == type_exercise_id)
            .order_by(func.random())
            # .distinct()
        )
    return rezult.scalars().all()


async def get_ex_muscules(session: AsyncSession, ex_id: int) -> list[Muscule]:
    rezult = await session.execute(
        select(Muscule)
            .join(Muscule.exercises)
            .where(Exercise.id == ex_id)
            .distinct()
        )
    return rezult.scalars().all()


async def get_last_user_workout_id(session: AsyncSession) -> int:
    rezult = await session.execute(select(UserWorkout).order_by(UserWorkout.id.desc()))
    rezult = rezult.scalars().first()
    return rezult.id if rezult is not None else None


# Добавление тренировки пользователя
async def add_new_user_workout(session: AsyncSession, user_id: int, user_workout_id: int) -> UserWorkout:
    user_workout: UserWorkout = UserWorkout(user_workout_id, user_id)
    session.add(user_workout)
    return user_workout


# Добавление упражнений тренировки пользователя
async def add_new_exs_user_workout(session: AsyncSession, exercises: list[ExerciseUserWorkout]) -> bool:
    rezult = False
    session.add_all(exercises)
    return True


# Получить  тренировки пользователя
async def get_last_user_workout(session: AsyncSession, user_id: int) -> UserWorkout:
    rezult = await session.execute(select(UserWorkout).where(UserWorkout.user_id == user_id).order_by(UserWorkout.id.desc()))
    return rezult.scalars().first()


async def get_user_exercises(session: AsyncSession, current_user_workout) -> Exercise:
    user_exercises: ExerciseUserWorkout = await session.execute(
        select(ExerciseUserWorkout)
            .where(ExerciseUserWorkout.train_id == current_user_workout)
            .order_by(ExerciseUserWorkout.number)
    )
    return user_exercises.scalars().all()
    # user_exercises = user_exercises.scalars().all()
    # user_id_exercises = [x.exercise_id for x in user_exercises]
    # rezult = await session.execute(
    #     select(Exercise)
    #         .where(Exercise.id.in_(user_id_exercises))
    # )
    # return rezult.scalars().all(), user_exercises