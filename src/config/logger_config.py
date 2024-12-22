import sys
from pathlib import Path

from loguru import logger


class LoggerConfig:
    """Класс конфигурации логгера."""

    LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "logs"

    def __init__(self, log_name: str, file_name: str, level: str = "INFO"):
        """Настраивает логгер с заданными параметрами.

        :param log_name: Имя логгера
        :param file_name: Имя файла лога.
        :param level: Уровень логирования (по умолчанию INFO).
        """
        logger.remove()
        self.log_dir = self.LOGS_DIR
        self.log_dir.mkdir(exist_ok=True)
        self.logger = logger.bind(name=log_name)

        # Настройка вывода в файл
        self.logger.add(
            self.log_dir / file_name,
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} | <level>{level: <8}</level> | {message}",
        )

        # Настройка вывода в консоль
        self.logger.add(
            sys.stdout,
            level=level,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        )

    def get_logger(self) -> logger:
        """Возвращает настроенный логгер."""
        return self.logger
