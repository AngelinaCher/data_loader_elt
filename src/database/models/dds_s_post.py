from sqlalchemy import TIMESTAMP, BigInteger, ForeignKeyConstraint, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class SatellitePost(Base):
    """Модель сателлита для постов."""

    __tablename__ = "s_post"
    __table_args__ = (
        ForeignKeyConstraint(["hub_post_hash_key"], ["dds.h_post.hub_post_hash_key"]),
        {"schema": "dds"},  # Указываем схему таблицы
    )

    hub_post_hash_key: Mapped[str] = mapped_column(String(255), nullable=False, primary_key=True)
    post_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    record_source: Mapped[str] = mapped_column(String, nullable=False)
    load_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now(), nullable=False, primary_key=True)
    hash_diff: Mapped[str] = mapped_column(String(255), nullable=True)
