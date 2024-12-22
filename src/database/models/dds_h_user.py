from sqlalchemy import TIMESTAMP, BigInteger, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class HubUser(Base):
    """Модель хаба для пользователей."""

    __tablename__ = "h_user"
    __table_args__ = {"schema": "dds"}

    hub_user_hash_key: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False)
    record_source: Mapped[str] = mapped_column(Text, nullable=False)
    load_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now(), nullable=False)
