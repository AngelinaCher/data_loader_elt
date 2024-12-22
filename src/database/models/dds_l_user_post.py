from sqlalchemy import TEXT, TIMESTAMP, ForeignKeyConstraint, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class LinkUserPost(Base):
    """Модель линка для связи постов и пользователей."""

    __tablename__ = "l_user_post"
    __table_args__ = (
        ForeignKeyConstraint(["hub_user_hash_key"], ["dds.h_user.hub_user_hash_key"]),
        ForeignKeyConstraint(["hub_post_hash_key"], ["dds.h_post.hub_post_hash_key"]),
        {"schema": "dds"},
    )

    hub_user_hash_key: Mapped[str] = mapped_column(String(255), nullable=False, primary_key=True)
    hub_post_hash_key: Mapped[str] = mapped_column(String(255), nullable=False, primary_key=True)
    record_source: Mapped[str] = mapped_column(TEXT, nullable=False)
    load_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now(), nullable=False, primary_key=True)
