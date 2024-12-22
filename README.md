# Data Loader ELT

Загрузка данных в слой DDS с использованием методологии Data Vault 2.0

## Описание

Данный проект демонстрирует процесс загрузки данных из REST API в корпоративное хранилище данных с использованием
методологии Data Vault 2.0. Данные хранятся в PostgreSQL.

## Структура проекта

* [logs](https://github.com/AngelinaCher/data_loader_elt/tree/master/logs) - логи
* [src](https://github.com/AngelinaCher/data_loader_elt/tree/master/src) - исходный код проекта
    + [config](https://github.com/AngelinaCher/data_loader_elt/tree/master/src/config) - конфигурационные файлы
        + [config.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/src/config/config.py)
        + [logger_config.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/src/config/logger_config.py) -
          настройки логгера
    + [database](https://github.com/AngelinaCher/data_loader_elt/tree/master/src/database) - подключение к БД, модели,
      скрипты для инициализации БД
        + [migrations](https://github.com/AngelinaCher/data_loader_elt/tree/master/src/database/migrations) - скрипты
          для инициализации БД
        + [models](https://github.com/AngelinaCher/data_loader_elt/tree/master/src/database/models) - модели
        + [connections.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/src/database/connections.py) -
          подключение к БД
        + [db_base.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/src/database/db_base.py) - создание
          Base
    + [elts](https://github.com/AngelinaCher/data_loader_elt/tree/master/src/elts) - скипты ELT
        + [elt1/api_to_stg.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/src/elts/elt1/api_to_stg.py) -
          elt процесс из API в слой STG
        + [elt2/stg_to_dds.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/src/elts/elt2/stg_to_dds.py) -
          elt процесс из STG в слой DDS
    + [schemas](https://github.com/AngelinaCher/data_loader_elt/tree/master/src/schemas) - модели Pydantic
    + [scripts](https://github.com/AngelinaCher/data_loader_elt/tree/master/src/scripts) - скрипты
        + [create_db.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/src/scripts/create_db.py) - скрипт
          для инициализации БД
    + [utils](https://github.com/AngelinaCher/data_loader_elt/tree/master/src/utils) - утилиты
        + [generate_hash.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/src/utils/generate_hash.py) -
          генерация хэшей
* [.env.template](https://github.com/AngelinaCher/data_loader_elt/blob/master/.env.template) - шаблон файла переменных
  окружения
* [.gitignore](https://github.com/AngelinaCher/data_loader_elt/blob/master/.gitignore) - игнорируемые файлы проекта
* [main.py](https://github.com/AngelinaCher/data_loader_elt/blob/master/main.py) - точка входа в приложение
* [pyproject.toml](https://github.com/AngelinaCher/data_loader_elt/blob/master/pyproject.toml) - конфигурационный файл
  проекта

## Требования

- Python 3.12 или выше
- PostgreSQL
- Библиотеки: `loguru`, `SQLAlchemy`, `requests` и другие зависимости, указанные в `requirements.txt`/`pyproject.toml`

## Установка проекта

1. Клонировать репозиторий

```bash
git clone git@github.com:AngelinaCher/data_loader_elt.git
```

```bash
cd data-loader-elt
```

2. Создать виртуальное окружние

```bash
python3 -m venv venv
```

3. Активировать виртуальное окружение
```bash
source venv/bin/activate
```

4. Установить зависимости
```bash
pip install -r requirements.txt
```

5. Добавить в проект файл `.env` и заполнить его своими данными по подобию `.env.template`
6. Запустить проект
```bash
python3 main.py
```

### Установка проекта с использованием Poetry
1. Клонировать репозиторий

```bash
git clone git@github.com:AngelinaCher/data_loader_elt.git
```

```bash
cd data_loader_elt
```

2. Создать и активировать виртуальное окружние 

```bash
poetry shell
```

3. Установить зависимости
```bash
poetry install
```

4. Добавить в проект файл `.env` и заполнить его своими данными по подобию `.env.template`
5. Запустить проект
```bash
python3 main.py
```