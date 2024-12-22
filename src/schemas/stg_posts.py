from pydantic import BaseModel, Field


class StgPostIn(BaseModel):
    """Модель Pydantic для таблицы `stg.posts`."""

    user_id: int = Field(..., alias="userId")
    id: int
    title: str
    body: str


class Config:
    """Конфигурация модели Pydantic для работы с SQLAlchemy с таблицей `stg.posts`."""

    orm_mode = True
