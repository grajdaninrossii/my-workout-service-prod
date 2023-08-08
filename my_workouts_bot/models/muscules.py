from sqlalchemy import BigInteger, Integer, String, Sequence, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import MappedAsDataclass, Mapped

from .base import Base


muscule_users_groups_table = Table(
    'muscule_users_groups',
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("muscules_id", ForeignKey("muscules.id", ondelete="CASCADE"), primary_key=True),
)


muscule_exercise_groups_table = Table(
    'muscule_exercise_groups',
    Base.metadata,
    Column("exercise_id", ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True),
    Column("muscules_id", ForeignKey("muscules.id", ondelete="CASCADE"), primary_key=True),
)


class Muscule(MappedAsDataclass, Base):
    __tablename__ = 'muscules'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    muscule_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    users: Mapped[list['User']] = relationship("User", secondary=muscule_users_groups_table, init=False, back_populates="muscules")
    exercises: Mapped[list['Exercise']] = relationship("Exercise", secondary=muscule_exercise_groups_table, init=False, back_populates="muscules", lazy='selectin', uselist=True)