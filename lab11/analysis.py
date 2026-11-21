def validate_todos(data):
    """Проверяет структуру набора. При нарушении бросает ValueError."""
    if not isinstance(data, list):
        raise ValueError("Корень JSON должен быть списком")

    seen_ids = set()
    for index, todo in enumerate(data):
        where = f"Запись {index}"
        if not isinstance(todo, dict):
            raise ValueError(f"{where}: ожидался объект")

        for key in ("id", "userId", "title", "completed"):
            if key not in todo:
                raise ValueError(f"{where}: отсутствует ключ {key!r}")

        if type(todo["id"]) is not int or todo["id"] <= 0:
            raise ValueError(f"{where}: id должен быть положительным целым")
        if type(todo["userId"]) is not int or todo["userId"] <= 0:
            raise ValueError(f"{where}: userId должен быть положительным целым")
        if not isinstance(todo["title"], str) or not todo["title"].strip():
            raise ValueError(f"{where}: title должен быть непустой строкой")
        if type(todo["completed"]) is not bool:
            raise ValueError(f"{where}: completed должен быть bool")

        if todo["id"] in seen_ids:
            raise ValueError(f"{where}: id {todo['id']} повторяется")
        seen_ids.add(todo["id"])
    return data


def completion_counts(todos):
    """Словарь userId → количество выполненных задач (для всех пользователей)."""
    counts = {}
    for todo in todos:
        user_id = todo["userId"]
        counts.setdefault(user_id, 0)
        if todo["completed"]:
            counts[user_id] += 1
    return counts


def top_users(counts):
    """Отсортированный список лидеров. Пусто при пустом словаре или максимуме 0."""
    if not counts:
        return []
    best = max(counts.values())
    if best == 0:
        return []
    return sorted(user_id for user_id, count in counts.items() if count == best)


def select_tasks(todos, user_id, parameter=None):
    """Вариант 8: задачи пользователя, у которых название содержит подстроку parameter.

    Поиск без учёта регистра. Порядок записей сохраняется, исходные записи не меняются.
    """
    result = []
    for todo in todos:
        if todo["userId"] != user_id:
            continue
        if parameter is not None:
            needle = parameter.lower()
            if needle not in todo["title"].lower():
                continue
        result.append(todo)
    return result