import sys

from loguru import logger

from src.config import LoggerConfig
from src.database import Session
from src.database.models import HubPost, HubUser, LinkUserPost, SatellitePost, SatelliteUser, StgPost
from src.schemas import PostIn, SatellitePostIn, SatelliteUserIn, UserIn, UserPostLinkIn
from src.utils import generate_hash


class StgToDdsLoader:
    """Класс для загрузки данных из слоя STG в DDS."""

    def __init__(self):
        """Инициализация класса загрузки данных в слой DDS."""
        self.session = Session()
        self.logger = self._init_logger()

    @staticmethod
    def _init_logger() -> logger:
        """Инициализация логгера."""
        logger_config = LoggerConfig(log_name="elt_logger", file_name="elt.log", level="INFO")
        elt_logger = logger_config.get_logger()

        return elt_logger

    def _fetch_stg_data(self) -> list | None:
        """Извлекает данные из STG.

        Возвращает сырой список данных о постах из таблицы `stg.posts`
        или завершает выполнение программы в случаи ошибки.

        :return: сырой список данных о постах
        """
        try:
            stg_posts = self.session.query(StgPost).all()

            if not stg_posts:
                logger.error("Нет данных для загрузки из STG")
                sys.exit(1)
            return stg_posts
        except Exception as e:
            logger.error(f"Ошибка при извлечении данных из STG: {e}")
            sys.exit(1)

    def _validate_and_create(self, pydantic_model, data_dict):
        """Валидирует данные через Pydantic и возвращает валидированный объект.

        :param pydantic_model: Pydantic-модель для валидации
        :param data_dict: cловарь данных для валидации
        :return: провалидированный объект модели
        """
        try:
            validated_data = pydantic_model(**data_dict)
            return validated_data
        except Exception as e:
            self.logger.error(f"Ошибка валидации данных: {e}")
            raise

    def _process_user(self, stg_post) -> str:
        """Обрабатывает хаб для пользователя и возвращает hub_user_hash_key.

        :param stg_post: запись из таблицы stg.posts
        :return: хэш для таблицы h_user
        """
        user_hash_key = generate_hash(str(stg_post.user_id))
        user = self.session.query(HubUser).filter_by(hub_user_hash_key=user_hash_key).first()

        if not user:
            user_data = {
                "hub_user_hash_key": user_hash_key,
                "user_id": stg_post.user_id,
                "record_source": stg_post.source,
                "load_date": stg_post.load_time,
            }
            validated_user = self._validate_and_create(UserIn, user_data)
            user = HubUser(**validated_user.model_dump())
            try:
                self.session.add(user)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                self.logger.error(f"Ошибка при вставке в h_user: {e}")

        return user_hash_key

    def _process_post(self, stg_post) -> str:
        """Обрабатывает хаб для поста и возвращает hub_post_hash_key.

        :param stg_post: запись из таблицы stg.posts
        :return: хэш для таблицы h_post
        """
        post_hash_key = generate_hash(str(stg_post.id))
        post = self.session.query(HubPost).filter_by(hub_post_hash_key=post_hash_key).first()

        if not post:
            post_data = {
                "hub_post_hash_key": post_hash_key,
                "post_id": stg_post.id,
                "record_source": stg_post.source,
                "load_date": stg_post.load_time,
            }
            validated_post = self._validate_and_create(PostIn, post_data)
            post = HubPost(**validated_post.model_dump())
            try:
                self.session.add(post)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                self.logger.error(f"Ошибка при вставке в h_post: {e}")

        return post_hash_key

    def _process_user_post_link(self, user_hash_key, post_hash_key, stg_post) -> None:
        """Обрабатывает линк для пользователя и поста.

        :param user_hash_key: хэш из таблицы h_user
        :param post_hash_key: хэш из таблицы h_post
        :param stg_post: запись из таблицы stg.posts
        :return:
        """
        link_data = {
            "hub_user_hash_key": user_hash_key,
            "hub_post_hash_key": post_hash_key,
            "record_source": stg_post.source,
            "load_date": stg_post.load_time,
        }
        validated_link = self._validate_and_create(UserPostLinkIn, link_data)
        link = LinkUserPost(**validated_link.model_dump())

        try:
            self.session.add(link)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Ошибка при вставке в l_user_post: {e}")

    def _process_user_satellite(self, user_hash_key, stg_post) -> None:
        """Обрабатывает сателлит для пользователя с дельта-обновлениями.

        :param user_hash_key: хэш из таблицы h_user
        :param stg_post: запись из таблицы stg.posts
        """
        user_satellite = self.session.query(SatelliteUser).filter_by(hub_user_hash_key=user_hash_key).first()
        new_user_hash_diff = generate_hash(str(stg_post.user_id))

        if not user_satellite or user_satellite.hash_diff != new_user_hash_diff:
            user_satellite_data = {
                "hub_user_hash_key": user_hash_key,
                "user_id": stg_post.user_id,
                "record_source": stg_post.source,
                "hash_diff": new_user_hash_diff,
                "load_date": stg_post.load_time,
            }
            validated_satellite = self._validate_and_create(SatelliteUserIn, user_satellite_data)
            user_satellite = SatelliteUser(**validated_satellite.model_dump())

            try:
                self.session.add(user_satellite)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                self.logger.error(f"Ошибка при вставке в s_user: {e}")

    def _process_post_satellite(self, post_hash_key, stg_post) -> None:
        """Обрабатывает сателлит для поста с дельта-обновлениями.

        :param post_hash_key: хэш из таблицы h_post
        :param stg_post: запись из таблицы stg.posts
        """
        post_satellite = self.session.query(SatellitePost).filter_by(hub_post_hash_key=post_hash_key).first()
        new_post_hash_diff = generate_hash(str(stg_post.title) + str(stg_post.body) + str(stg_post.id))

        if not post_satellite or post_satellite.hash_diff != new_post_hash_diff:
            post_satellite_data = {
                "hub_post_hash_key": post_hash_key,
                "post_id": stg_post.id,
                "title": stg_post.title,
                "body": stg_post.body,
                "record_source": stg_post.source,
                "hash_diff": new_post_hash_diff,
                "load_date": stg_post.load_time,
            }
            validated_satellite = self._validate_and_create(SatellitePostIn, post_satellite_data)
            post_satellite = SatellitePost(**validated_satellite.model_dump())

            try:
                self.session.add(post_satellite)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                self.logger.error(f"Ошибка при вставке в s_post: {e}")

    def _load_data_to_dds(self, stg_posts) -> None:
        """Основной метод для загрузки данных в DDS.

        :param stg_posts: извлеченные записи с сырами данными из `stg.posts`.
        """
        for stg_post in stg_posts:
            user_hash_key = self._process_user(stg_post)
            post_hash_key = self._process_post(stg_post)
            self._process_user_post_link(user_hash_key, post_hash_key, stg_post)
            self._process_user_satellite(user_hash_key, stg_post)
            self._process_post_satellite(post_hash_key, stg_post)

        try:
            self.session.commit()
            self.logger.info("Данные успешно загружены в слой DDS.")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Ошибка при загрузке данных в слой DDS: {e}")

    def run(self):
        """Запускает скрипт для загрузки данных из STG в слой DDS.

        Получает данные из таблицы `stg.posts`, валидирует их и загружает данные
        по хабам, линкам и сателлитам.
        """
        stg_posts = self._fetch_stg_data()
        self._load_data_to_dds(stg_posts)


if __name__ == "__main__":
    stg_to_dds_loader = StgToDdsLoader()
    stg_to_dds_loader.run()
