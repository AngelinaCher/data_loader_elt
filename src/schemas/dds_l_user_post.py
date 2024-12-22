from datetime import datetime

from pydantic import BaseModel


class UserPostLinkIn(BaseModel):
    """Модель Pydantic для таблицы `dds.l_user_post`."""

    hub_user_hash_key: str
    hub_post_hash_key: str
    record_source: str
    load_date: datetime

    class Config:
        """Конфигурация модели Pydantic для работы с SQLAlchemy с таблицей `dds.l_user_post`."""

        from_attributes = True
