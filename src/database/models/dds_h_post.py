from sqlalchemy import TEXT, TIMESTAMP, BigInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class HubPost(Base):
    """Модель хаба для постов."""

    __tablename__ = "h_post"
    __table_args__ = {"schema": "dds"}

    hub_post_hash_key: Mapped[str] = mapped_column(String(255), primary_key=True)
    post_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False)
    record_source: Mapped[str] = mapped_column(TEXT, nullable=False)
    load_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now(), nullable=False)
