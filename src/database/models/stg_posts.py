from sqlalchemy import TIMESTAMP, BigInteger, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class StgPost(Base):
    """Модель таблицы posts схемы stg."""

    __tablename__ = "posts"
    __table_args__ = {"schema": "stg"}

    stg_id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        __name_pos="userId",
        nullable=False,
    )
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    load_time: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now(), nullable=False)
