import json
from pathlib import Path

from analysis import (
    validate_todos,
    completion_counts,
    top_users,
    select_tasks,
)


FOLDER = Path(__file__).resolve().parent
SOURCE = FOLDER / "todos.json"
LEADERS = FOLDER / "leaders.json"
SELECTED = FOLDER / "selected.json"


def read_positive_integer(prompt):
    """Повторяет ввод, пока не получено целое > 0."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Это не целое число, повторите")
            continue
        if value <= 0:
            print("Число должно быть больше нуля")
            continue
        return value


def read_nonempty_text(prompt):
    """Повторяет ввод, пока не получена непустая строка после strip()."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Строка не должна быть пустой")


def leader_completed_tasks(todos, leader_ids):
    """Завершённые задачи лидеров в исходном порядке."""
    leader_set = set(leader_ids)
    return [
        todo for todo in todos
        if todo["userId"] in leader_set and todo["completed"]
    ]


def load_todos(path):
    """Читает todos.json. Ошибки формата и доступа — исключениями, для main()."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def main():
    user_id = read_positive_integer("Введите user_id: ")
    substring = read_nonempty_text("Введите подстроку для поиска в названии: ")

    # Читаем и проверяем вход ДО любой записи результатов.
    try:
        data = load_todos(SOURCE)
    except FileNotFoundError:
        print(f"Файл не найден: {SOURCE}")
        return
    except UnicodeError:
        print("Не удалось прочитать файл в кодировке UTF-8")
        return
    except json.JSONDecodeError as error:
        print(f"Некорректный JSON: {error}")
        return
    except OSError as error:
        print(f"Ошибка доступа к файлу: {error}")
        return

    try:
        validate_todos(data)
    except ValueError as error:
        print(f"Некорректная структура данных: {error}")
        return

    counts = completion_counts(data)
    leaders = top_users(counts)
    leader_tasks = leader_completed_tasks(data, leaders)
    selected = select_tasks(data, user_id, substring)

    try:
        save_json(LEADERS, leader_tasks)
        save_json(SELECTED, selected)
    except OSError as error:
        print(f"Не удалось записать результаты: {error}")
        return

    print("Количества завершённых:", counts)
    print("Лидеры:", leaders)
    print("Задачи лидеров:", [todo["id"] for todo in leader_tasks])
    print(
        f"Выборка для user_id={user_id}, подстрока={substring!r}:",
        [todo["id"] for todo in selected],
    )


if __name__ == "__main__":
    main()