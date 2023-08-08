from pydantic import BaseModel, Field

from models import Muscule, TypeExercise, Inventory


class ExerciseSchema(BaseModel):
    __tablename__ = 'exercises'

    ex_id: int
    approach_count: int
    values: str = Field(default="10")
    relax_time: int = Field(default=60)

    class Config:
        orm_mode = True