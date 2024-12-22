from datetime import datetime

from pydantic import BaseModel


class UserIn(BaseModel):
    """Модель Pydantic для таблицы `dds.h_user`."""

    hub_user_hash_key: str
    user_id: int
    record_source: str
    load_date: datetime

    class Config:
        """Конфигурация модели Pydantic для работы с SQLAlchemy с таблицей `dds.h_user`."""

        from_attributes = True
