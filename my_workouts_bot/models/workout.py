from sqlalchemy import BigInteger, Integer, String, ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import MappedAsDataclass, Mapped
from datetime import datetime

# from user import User
# from exercise import Exercises

from .base import Base


# Данные тестовой тренировки
# exam_workout_table = Table(
#     "exam_workouts",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
#     Column("exercise_id", ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True),
#     Column("values", String(255)),
# )

class ExamWorkout(MappedAsDataclass, Base):
    __tablename__ = "exam_workouts"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, init=False)
    exercise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True, init=False)
    values: Mapped[str] = mapped_column(String(255), default=None, init=True)

    user: Mapped['User'] = relationship("User", backref="users", init=False)
    exercise: Mapped['Exercise'] = relationship("Exercise", backref="exercises", init=False)


class ExerciseUserWorkout(MappedAsDataclass, Base):
    __tablename__ = "exercise_user_workouts"

    train_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user_workouts.id", ondelete="CASCADE"), primary_key=True, init=True)
    exercise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True, init=True)
    approach_count: Mapped[int] = mapped_column(Integer, default=None, init=True, nullable=True)
    values: Mapped[str] = mapped_column(String(255), default=None, init=True)
    relax_time: Mapped[int] = mapped_column(Integer, default=None, init=True)
    number: Mapped[int] = mapped_column(Integer, default=None, init=True, nullable=True)

    user_workout: Mapped['UserWorkout'] = relationship("UserWorkout", backref="user_workouts", init=False)
    user_exercise: Mapped['Exercise'] = relationship("Exercise", backref="user_exercises", init=False, lazy='selectin')
    # null, 2, 3, 10, 60

# # Упражнения в пользовательских тренировках
# exercise_user_workout_table = Table(
#     "exercise_user_workouts",
#     Base.metadata,
#     Column("train_id", ForeignKey("user_workouts.id", ondelete="CASCADE"), primary_key=True),
#     Column("exercise_id", ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True),
#     Column("approach_count", Integer),
#     Column("values", String(255)),
#     Column("relax_time", Integer),
# )


# Тренировки пользователя
class UserWorkout(MappedAsDataclass, Base):
    __tablename__ = 'user_workouts'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped['User'] = relationship('User', default=None, init=False)

    user_exercises:Mapped[list['ExerciseUserWorkout']] = relationship('ExerciseUserWorkout', default=None, backref="user_workouts", init=False)



class TypesWorkout(MappedAsDataclass, Base):
    __tablename__ = 'type_workouts'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    type_name: Mapped[str] = mapped_column(String(255), unique=True)


# Сохранение информации о тренировке
class CalendarStatistics(MappedAsDataclass, Base):
    __tablename__ = 'calendar_statistics'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), default=None)
    user: Mapped["User"] = relationship("User", default=None, init=False)

    type_workout_id: Mapped["TypesWorkout"] = mapped_column(Integer, ForeignKey("type_workouts.id", ondelete="CASCADE"), default=None)
    review_id: Mapped[int] = mapped_column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), default=None)
    feeling_id: Mapped[int] = mapped_column(Integer, ForeignKey("feelings.id", ondelete="CASCADE"), default=None)
    training_date: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.utcnow())


class Feeling(MappedAsDataclass, Base):
    __tablename__ = 'feelings'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    feeling_name: Mapped[str] = mapped_column(String(255), unique=True)


class Review(MappedAsDataclass, Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    review_name: Mapped[str] = mapped_column(String(255), unique=True)