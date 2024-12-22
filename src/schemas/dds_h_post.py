from datetime import datetime

from pydantic import BaseModel


class PostIn(BaseModel):
    """Модель Pydantic для таблицы `dds.h_post`."""

    hub_post_hash_key: str
    post_id: int
    record_source: str
    load_date: datetime

    class Config:
        """Конфигурация модели Pydantic для работы с SQLAlchemy с таблицей `dds.h_post`."""

        from_attributes = True
