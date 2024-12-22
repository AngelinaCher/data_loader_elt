import json
import sys

import requests

from src.config import LoggerConfig
from src.database import Session
from src.database.models import StgPost
from src.schemas import StgPostIn


class ApiExtractor:
    """Класс для извлечения данных из API и загрузки в слой STG."""

    API_URL = "https://jsonplaceholder.typicode.com/posts/"

    def __init__(self):
        """Инициализация класса для извлечения данных из API и сохранения их в STG."""
        self.session = Session()
        self.logger = self._init_logger()

    @staticmethod
    def _init_logger():
        logger_config = LoggerConfig(log_name="elt_logger", file_name="elt.log", level="INFO")
        logger = logger_config.get_logger()

        return logger

    def _fetch_data_from_api(self) -> json:
        """Получает данные из API.

        :return: данные в формате JSON
        """
        try:
            response = requests.get(self.API_URL)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка при запросе данных из API: {e}")
            return None

    def _validate_post_data(self, post_data: dict) -> StgPostIn | None:
        """Валидирует данные из API.

        :param post_data: данные поста для валидации
        :return:
        """
        try:
            stg_post = StgPostIn(**post_data)
            return stg_post
        except Exception as e:
            self.logger.warning(f"Ошибка валидации поста: {post_data} | Ошибка: {e}")
            return None

    @staticmethod
    def _create_stg_post_model(stg_post: StgPostIn) -> StgPost:
        """Создает модель.

        :param stg_post: провалидированные данные поста
        :return:
        """
        stg_post_data = stg_post.model_dump(by_alias=True)  # Получаем словарь с учетом alias

        return StgPost(
            user_id=stg_post_data["userId"],
            id=stg_post_data["id"],
            title=stg_post_data["title"],
            body=stg_post_data["body"],
            source="API",
        )

    def _add_to_session(self, stg_post_model: StgPost) -> None:
        """Добавляет модель в сессию.

        :param stg_post_model: модель таблицы sql.post
        :return:
        """
        self.session.add(stg_post_model)

    def _commit_to_db(self) -> None:
        """Коммит данных в базу."""
        try:
            self.session.commit()
            self.logger.info("Успешно загружено записей в STG.")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Ошибка при сохранении данных в STG: {e}")
            sys.exit(1)

    def _load_data_to_stg(self, posts: list[dict]) -> None:
        """Загружает данные в слой STG без трансформации.

        :param posts: полученные посты из API
        :return:
        """
        if not posts:
            self.logger.error("Отсутствуют данные для добавления")
            sys.exit(1)

        for post_data in posts:
            stg_post = self._validate_post_data(post_data)
            if stg_post:
                stg_post_model = self._create_stg_post_model(stg_post)
                try:
                    self._add_to_session(stg_post_model)
                except Exception as ex:
                    self.logger.error(f"Ошибка при добавлении данных в сессию: {ex}")
        self._commit_to_db()

    def run(self):
        """Запускает скрипт для загрузки данных из API в слой STG."""
        data = self._fetch_data_from_api()
        self._load_data_to_stg(data)


if __name__ == "__main__":
    api_extractor = ApiExtractor()
    api_extractor.run()
