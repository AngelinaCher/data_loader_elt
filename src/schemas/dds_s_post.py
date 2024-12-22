from datetime import datetime

from pydantic import BaseModel


class SatellitePostIn(BaseModel):
    """Модель Pydantic для таблицы `dds.s_post`."""

    hub_post_hash_key: str
    post_id: int
    title: str
    body: str
    record_source: str
    load_date: datetime
    hash_diff: str

    class Config:
        """Конфигурация модели Pydantic для работы с SQLAlchemy с таблицей `dds.s_post`."""

        from_attributes = True
