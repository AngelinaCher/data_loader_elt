import sys
from pathlib import Path

from loguru import logger
from sqlalchemy.sql import text

from src.config import LoggerConfig
from src.database import Session


def execute_sql_file(logger: logger, file_path: str) -> None:
    """Исполняет SQL команды из файла.

    :param logger: экземпляр логгера
    :param file_path: путь до файла с sql-запросом
    """
    session = Session()
    print(type(logger))
    with open(file_path, "r") as f:
        sql_script = f.read()
    with session as connection:
        try:
            connection.execute(text(sql_script))
            connection.commit()
        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса {file_path}: {e}")
            raise


def get_sorted_sql_scripts(sql_scripts_dir: Path) -> list[Path]:
    """Возвращает отсортированный список SQL файлов из директории.

    :param sql_scripts_dir: путь до директории с SQL-скриптами
    :return: список путей до SQL-скриптов
    """
    if not sql_scripts_dir.exists():
        raise FileNotFoundError(f"Папка с миграциями не найдена: {sql_scripts_dir}")
    return sorted(sql_scripts_dir.glob("*.sql"))


def process_sql_scripts(logger: logger, sql_scripts: list[Path]) -> None:
    """Последовательно выполняет список SQL скриптов.

    :param logger: экземпляр логгера
    :param sql_scripts: список путей до SQL-скриптов
    """
    for script in sql_scripts:
        script_name = script.name
        logger.info(f"Выполнение: {script_name}")
        try:
            execute_sql_file(logger, script)
            logger.info(f"Успешное выполнение: {script_name}")
        except Exception as e:
            logger.error(f"Ошибка при выполнении {script_name}: {e}")
            sys.exit(1)


def init_db(logger: logger):
    """Инициализация базы данных: создание схем, хабов, линков, сателлитов.

    :param logger: экземпляр логгера
    """
    sql_scripts_dir = Path(__file__).resolve().parent.parent / "database" / "migrations"
    try:
        sql_scripts = get_sorted_sql_scripts(sql_scripts_dir)
        process_sql_scripts(logger, sql_scripts)
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    loger_config = LoggerConfig(log_name="db_logger", file_name="database.log", level="INFO")
    logger = loger_config.get_logger()

    init_db(logger)
    logger.info("База данных инициализована успешно")
