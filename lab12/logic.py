"""Логика работы с записями. Не читает файлы и не общается с пользователем."""

REQUIRED_KEYS = ("id", "title", "category", "amount", "completed")


def validate_records(records):
    """Проверяет список записей. Возвращает records. При нарушении бросает ValueError."""
    if not isinstance(records, list):
        raise ValueError("Корень JSON должен быть списком")

    seen_ids = set()
    for index, record in enumerate(records):
        where = f"Запись {index}"
        if not isinstance(record, dict):
            raise ValueError(f"{where}: ожидался объект")

        for key in REQUIRED_KEYS:
            if key not in record:
                raise ValueError(f"{where}: отсутствует ключ {key!r}")

        if type(record["id"]) is not int or record["id"] <= 0:
            raise ValueError(f"{where}: id должен быть положительным целым")
        if record["id"] in seen_ids:
            raise ValueError(f"{where}: id {record['id']} повторяется")
        seen_ids.add(record["id"])

        if not isinstance(record["title"], str) or not record["title"].strip():
            raise ValueError(f"{where}: title должен быть непустой строкой")
        if not isinstance(record["category"], str) or not record["category"].strip():
            raise ValueError(f"{where}: category должна быть непустой строкой")
        if type(record["amount"]) is not int or record["amount"] < 0:
            raise ValueError(f"{where}: amount должен быть целым неотрицательным")
        if type(record["completed"]) is not bool:
            raise ValueError(f"{where}: completed должен быть bool")
    return records


def next_id(records):
    """Следующий id: max существующих + 1, или 1 для пустого списка."""
    if not records:
        return 1
    return max(record["id"] for record in records) + 1


def add_record(records, title, category, amount):
    """Добавляет запись (completed=False) и возвращает её. Изменяет список records."""
    title = title.strip()
    category = category.strip()
    if not title:
        raise ValueError("Название не должно быть пустым")
    if not category:
        raise ValueError("Категория не должна быть пустой")
    if type(amount) is not int or amount < 0:
        raise ValueError("Количество должно быть целым неотрицательным")

    record = {
        "id": next_id(records),
        "title": title,
        "category": category,
        "amount": amount,
        "completed": False,
    }
    records.append(record)
    return record


def find_records(records, query):
    """Записи, в названии которых есть query без учёта регистра. Исходный список не меняется."""
    needle = query.strip().lower()
    if not needle:
        raise ValueError("Поисковый запрос не должен быть пустым")
    return [record for record in records if needle in record["title"].lower()]


def set_completed(records, record_id, completed):
    """True при успехе, False при неизвестном id. Изменяет список при успехе."""
    if type(completed) is not bool:
        raise ValueError("completed должен быть bool")
    for record in records:
        if record["id"] == record_id:
            record["completed"] = completed
            return True
    return False


def delete_record(records, record_id):
    """True при успехе, False при неизвестном id. Изменяет список при успехе."""
    for index, record in enumerate(records):
        if record["id"] == record_id:
            del records[index]
            return True
    return False


def statistics(records):
    """Словарь со статистикой. Исходный список не меняется."""
    total = len(records)
    completed = sum(1 for record in records if record["completed"])
    by_category = {}
    for record in records:
        category = record["category"].strip()
        by_category[category] = by_category.get(category, 0) + record["amount"]
    return {
        "total": total,
        "completed": completed,
        "not_completed": total - completed,
        "amount_sum": sum(record["amount"] for record in records),
        "by_category": by_category,
    }