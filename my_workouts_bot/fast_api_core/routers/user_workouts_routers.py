from fastapi import APIRouter, Depends, Request


user_workouts_router = APIRouter() #prefix="/user_workouts"
from config.settings import templates
from config.logger import logging
from repositories import ex_repo
from models import async_session
from fast_api_core.schemas.exericse_schema import ExerciseSchema
from utils import loop


async def get_all_exercises() -> list:
    async with async_session() as session:
        all_exercises: list[ExerciseSchema] = [ExerciseSchema.from_orm(ex) for ex in sorted(await ex_repo.get_all_exercises(session), key=lambda x: x.type_exercise_id)]
    return all_exercises


@user_workouts_router.get("/add_user_workout")
async def add_user_workouts_temp(request: Request):
    return templates.TemplateResponse(
        name='add_user_workout.html',
        context={
            'request': request,
            'exercises': exercises,
            'count_ex': len(exercises)
        }
    )

exercises = loop.run_until_complete(get_all_exercises())