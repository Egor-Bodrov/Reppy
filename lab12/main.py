"""Консольное меню варианта 8: план туристических маршрутов."""

from pathlib import Path

from logic import (
    add_record,
    delete_record,
    find_records,
    set_completed,
    statistics,
    validate_records,
)
from storage import load_records, save_records


DATA = Path(__file__).resolve().parent / "data.json"
UNIT = "км"
MENU = (
    "1. Показать записи\n"
    "2. Добавить запись\n"
    "3. Найти записи\n"
    "4. Изменить статус\n"
    "5. Удалить запись\n"
    "6. Показать статистику\n"
    "7. Сохранить данные\n"
    "8. Выйти"
)


def format_record(record):
    status = "пройден" if record["completed"] else "не пройден"
    return (
        f"#{record['id']:>3} | {record['title']:<25} | "
        f"{record['category']:<12} | {record['amount']:>4} {UNIT} | {status}"
    )


def read_int(prompt, minimum=0):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Это не целое число, повторите")
            continue
        if value < minimum:
            print(f"Значение должно быть не меньше {minimum}")
            continue
        return value


def read_nonempty(prompt):
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Строка не должна быть пустой")


def read_bool(prompt):
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("да", "yes", "y", "1"):
            return True
        if raw in ("нет", "no", "n", "0"):
            return False
        print("Ответьте «да» или «нет»")


def do_show(records):
    if not records:
        print("Нет записей")
        return
    for record in sorted(records, key=lambda r: r["id"]):
        print(format_record(record))


def do_add(records):
    title = read_nonempty("Название: ")
    category = read_nonempty("Категория: ")
    amount = read_int("Длина в км (целое >= 0): ", minimum=0)
    record = add_record(records, title, category, amount)
    print(f"Добавлена запись #{record['id']}: {record['title']}")


def do_find(records):
    query = read_nonempty("Подстрока для поиска: ")
    found = find_records(records, query)
    if not found:
        print("Ничего не найдено")
        return
    for record in sorted(found, key=lambda r: r["id"]):
        print(format_record(record))


def do_set_status(records):
    record_id = read_int("ID записи: ", minimum=1)
    completed = read_bool("Отметить как «пройден»? (да/нет): ")
    if set_completed(records, record_id, completed):
        print(f"Статус записи #{record_id} обновлён")
    else:
        print(f"Запись #{record_id} не найдена, данные не изменены")


def do_delete(records):
    record_id = read_int("ID записи для удаления: ", minimum=1)
    if not any(record["id"] == record_id for record in records):
        print(f"Запись #{record_id} не найдена, данные не изменены")
        return
    if not read_bool(f"Удалить запись #{record_id}? (да/нет): "):
        print("Удаление отменено")
        return
    delete_record(records, record_id)
    print(f"Запись #{record_id} удалена")


def do_statistics(records):
    stats = statistics(records)
    print(f"Всего записей: {stats['total']}")
    print(f"Пройдено:      {stats['completed']}")
    print(f"Не пройдено:   {stats['not_completed']}")
    print(f"Сумма длин:    {stats['amount_sum']} {UNIT}")
    if not stats["by_category"]:
        print("Категорий нет")
        return
    print("По категориям:")
    for category in sorted(stats["by_category"]):
        print(f"  {category}: {stats['by_category'][category]} {UNIT}")


def do_save(records):
    try:
        save_records(DATA, records)
    except OSError as error:
        print(f"Не удалось сохранить: {error}")
        return False
    print("Данные сохранены:", DATA)
    return True


def try_load():
    """Возвращает список записей или None, если файл повреждён (запуск прекращается)."""
    try:
        return load_records(DATA)
    except FileNotFoundError:
        print(f"Файл {DATA.name} не найден, начинаем с пустого списка")
        return []
    except UnicodeError:
        print("Файл не читается как UTF-8, запуск прекращён")
        return None
    except OSError as error:
        print(f"Ошибка доступа к файлу: {error}, запуск прекращён")
        return None
    except ValueError as error:
        print(f"Некорректный формат данных: {error}, запуск прекращён")
        return None


def main():
    records = try_load()
    if records is None:
        return

    actions = {
        "1": do_show,
        "2": do_add,
        "3": do_find,
        "4": do_set_status,
        "5": do_delete,
        "6": do_statistics,
        "7": do_save,
    }

    while True:
        print("\n" + MENU)
        choice = input("Выберите пункт: ").strip()

        if choice == "8":
            while True:
                answer = input("Сохранить перед выходом? (да/нет): ").strip().lower()
                if answer in ("да", "yes", "y", "1"):
                    if do_save(records):
                        return
                    break  # ошибка записи — остаться в меню
                if answer in ("нет", "no", "n", "0"):
                    print("Выход без сохранения")
                    return
                print("Ответьте «да» или «нет»")
            continue

        action = actions.get(choice)
        if action is None:
            print("Неизвестная команда, повторите выбор")
            continue
        action(records)


if __name__ == "__main__":
    main()