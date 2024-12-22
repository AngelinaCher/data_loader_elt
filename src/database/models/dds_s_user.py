from sqlalchemy import TEXT, TIMESTAMP, BigInteger, ForeignKeyConstraint, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class SatelliteUser(Base):
    """Модель сателлита для пользователей."""

    __tablename__ = "s_user"
    __table_args__ = (
        ForeignKeyConstraint(["hub_user_hash_key"], ["dds.h_user.hub_user_hash_key"]),
        {"schema": "dds"},
    )

    hub_user_hash_key: Mapped[str] = mapped_column(String(255), nullable=False, primary_key=True)
    user_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False)
    record_source: Mapped[str] = mapped_column(TEXT, nullable=False)
    load_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now(), nullable=False, primary_key=True)
    hash_diff: Mapped[str] = mapped_column(String(255), nullable=True)
