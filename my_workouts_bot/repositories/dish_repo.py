from sqlalchemy import select, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi_asyncalchemy.models import *

from models import Dish

async def get_one_dish(session: AsyncSession, dish_id: int) -> Dish:
    rezult = await session.get(Dish, dish_id)
    return rezult


async def get_all_dishes(session: AsyncSession) -> list:
    rezult = await session.execute(
        select(
            Dish.id,
            Dish.title,
            Dish.kilocalories,
            Dish.proteins,
            Dish.fats,
            Dish.carbohydrates,
            Dish.is_piece,
            Dish.category,
            Dish.default_weight,
            Dish.max_weight
        )
    )
    return rezult.all()