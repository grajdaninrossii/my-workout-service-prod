from sqlalchemy import BigInteger, Integer, String, Sequence, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import MappedAsDataclass, Mapped

from .base import Base
from .muscules import muscule_exercise_groups_table


# Типы упражнений
class TypeExercise(MappedAsDataclass, Base):
    __tablename__ = 'types_workout_exercise'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    type_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # exercises: Mapped[list["Exercise"]] = relationship()



# Виды сложности (для упражнений)
class ComplexityLevel(MappedAsDataclass, Base):
    __tablename__ = 'complexity_levels'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    compl_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # exercises: Mapped[list["Exercise"]] = relationship()


# Интвентарь
class Inventory(MappedAsDataclass, Base):
    __tablename__ = 'inventories'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    inv_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # exercises: Mapped[list["Exercise"]] = relationship()


# # Типы значений для упражнений (кол-во/время)
# class TypeValueExercise(MappedAsDataclass, Base):
#     __tablename__ = 'types_value_exercise'

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
#     val_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
#     exercises: Mapped[list["Exercise"]] = relationship(back_populates="type_value_exercise") # двунаправленная связь


# Упражнения
class Exercise(MappedAsDataclass, Base):
    __tablename__ = 'exercises'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    ex_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    complexity_level_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("complexity_levels.id", ondelete="CASCADE"), default=None)
    complexity_level: Mapped['ComplexityLevel'] = relationship("ComplexityLevel", default=None)

    type_exercise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("types_workout_exercise.id", ondelete="CASCADE"), default=None)
    type_exercise: Mapped['TypeExercise'] = relationship("TypeExercise", default=None, lazy='selectin')

    inventories_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("inventories.id", ondelete="CASCADE"), default=None)
    inventories: Mapped['Inventory'] = relationship("Inventory", default=None, lazy='selectin')

    # type_value_exercise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("types_value_exercise.id", ondelete="CASCADE"), default=None)
    # type_value_exercise: Mapped['TypeValueExercise'] = relationship("TypeValueExercise", default=None, back_populates="exercises") # двунаправленная связь

    description: Mapped[str] = mapped_column(Text, default=None)
    technices: Mapped[str] = mapped_column(Text, default=None)
    image_exercise_url: Mapped[str] = mapped_column(String, default=None)

    muscules: Mapped[list['Muscule']] = relationship("Muscule", secondary=muscule_exercise_groups_table, init=False, back_populates="exercises", lazy='selectin', uselist=True)
    user_workouts:Mapped[list['ExerciseUserWorkout']] = relationship('ExerciseUserWorkout', default=None, init=False, backref="exercises")

    #!!!!
    # users: Mapped[list['User']] = relationship("User", secondary=exam_workout_table, init=False, back_populates="exercises")
    users: Mapped[list['ExamWorkout']] = relationship("ExamWorkout", default=None, init=False, backref="exercises")