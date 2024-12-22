from datetime import datetime

from pydantic import BaseModel


class SatelliteUserIn(BaseModel):
    """Модель Pydantic для таблицы `dds.l_user_post`."""

    hub_user_hash_key: str
    user_id: int
    record_source: str
    load_date: datetime
    hash_diff: str

    class Config:
        """Конфигурация модели Pydantic для работы с SQLAlchemy с таблицей `dds.l_user_post`."""

        from_attributes = True
