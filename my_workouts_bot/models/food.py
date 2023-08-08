from sqlalchemy import BigInteger, Integer, String, Sequence, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import MappedAsDataclass, Mapped

from .base import Base


class Dish(MappedAsDataclass, Base):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, init=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), default=None, nullable=False, unique=True, init=True)
    kilocalories: Mapped[float] = mapped_column(Float, default=None, init=False)
    proteins: Mapped[float] = mapped_column(Float, default=None, init=False)
    fats: Mapped[float] = mapped_column(Float, default=None, init=False)
    carbohydrates: Mapped[float] = mapped_column(Float, default=None, init=False)
    is_piece: Mapped[bool] = mapped_column(Boolean, default=None, init=False)
    category: Mapped[int] = mapped_column(Integer, default=None, init=False)
    default_weight: Mapped[int] = mapped_column(Integer, default=None, init=False)
    max_weight: Mapped[int] = mapped_column(Integer, default=None, init=False)
    recipe: Mapped[int] = mapped_column(Text, default=None, nullable=True, init=False)