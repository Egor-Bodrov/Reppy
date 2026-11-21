"""Чтение и запись JSON. Без консольных диалогов."""

import json
from pathlib import Path

from logic import validate_records


def load_records(path):
    """Возвращает список записей. FileNotFoundError — файла нет.

    json.JSONDecodeError / ValueError — неверный формат. Файл не перезаписывается.
    """
    path = Path(path)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return validate_records(data)


def save_records(path, records):
    """Записывает records в JSON. Бросает OSError при ошибке записи."""
    path = Path(path)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)