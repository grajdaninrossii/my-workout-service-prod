from sqlalchemy import BigInteger, Integer, String, Sequence, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import MappedAsDataclass, Mapped

from .base import Base


# Советы по тренировкам и питанию
class Advice(MappedAsDataclass, Base):
    __tablename__ = 'advices'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories_advices.id", ondelete="CASCADE"), default=None)
    category: Mapped['CategoryAdvice'] = relationship("CategoryAdvice", default=None)

    text: Mapped[str] = mapped_column(Text, default=None, unique=True, nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, default=None)
    source_url: Mapped[str] = mapped_column(String(255), nullable=False, default=None)


# Категории советов(питание, тренировки, организация)
class CategoryAdvice(MappedAsDataclass, Base):
    __tablename__ = 'categories_advices'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, init=False)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)