from pydantic import BaseModel, Field

from models import Muscule, TypeExercise, Inventory


class ExerciseSchema(BaseModel):
    __tablename__ = 'exercises'

    id: int
    ex_name: str
    complexity_level_id: int

    type_exercise: TypeExercise
    inventories: Inventory
    description: str
    technices: str
    image_exercise_url: str

    class Config:
        orm_mode = True