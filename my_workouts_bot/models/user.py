from datetime import datetime
from sqlalchemy import BigInteger, Integer, String, Sequence, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import MappedAsDataclass, Mapped

from .base import Base
# from .workout import exam_workout_table
from .muscules import muscule_users_groups_table


class Goal(MappedAsDataclass, Base):
    __tablename__ = 'goals'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, init=False, unique=True)
    goal_name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    # users: Mapped[list['User']] = relationship()


class Gender(MappedAsDataclass, Base):
    __tablename__ = 'genders'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, init=False, unique=True)
    gender_name: Mapped[str]= mapped_column(String(40), nullable=False, unique=True)
    # users: Mapped[list['User']] = relationship()


class User(MappedAsDataclass, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False, unique=True)
    # name = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255), default=None, nullable=False) # ????
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, init=False)

    height: Mapped[int] = mapped_column(Integer, default=None, init=False, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, default=None, init=False, nullable=True)
    age: Mapped[int] = mapped_column(Integer, default=None, init=True, nullable=True)
    is_agree: Mapped[int] = mapped_column(Boolean, default=False, nullable=False, init=False)

    goal_id: Mapped[int] = mapped_column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), default=None, init=False, nullable=True)
    goal:Mapped['Goal'] = relationship("Goal", default=None, init=False, lazy='selectin')

    rate: Mapped[int] = mapped_column(Integer, default=None, init=False, nullable=True)

    # calendar_statistics: Mapped[list["CalendarStatistics"]] = relationship()

    gender_id: Mapped[int] = mapped_column(Integer, ForeignKey("genders.id", ondelete="CASCADE"), default=None, init=False, nullable=True)
    gender: Mapped['Gender'] = relationship("Gender", default=None, init=False, lazy='selectin')
    # number: Mapped[int] = mapped_column(Integer, default=None, init=True, nullable=True)


    # exercises: Mapped[list['Exercise']] = relationship("Exercise", secondary=exam_workout_table, init=False, back_populates="users")
    exercises: Mapped[list['ExamWorkout']] = relationship("ExamWorkout", init=False, backref="users", lazy='selectin', uselist=True)
    muscules: Mapped[list['Muscule']] = relationship("Muscule", secondary=muscule_users_groups_table, init=False, back_populates="users")
