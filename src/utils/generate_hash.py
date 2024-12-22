import hashlib


def generate_hash(input_string: str) -> str:
    """Генерирует SHA-256 хеш для строки.

    :param input_string: строка для хэширования
    :return: хэш строки
    """
    hash_object = hashlib.sha256()
    try:
        hash_object.update(input_string.encode("utf-8"))
    except Exception as e:
        raise f"Не удалось захэшировать строку, возникла ошибка: {e}"

    return hash_object.hexdigest()
