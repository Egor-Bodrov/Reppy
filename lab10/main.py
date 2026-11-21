from pathlib import Path

from files_lab import read_matrix, selected_sum
from table import row_sums, column_sums


FOLDER = Path(__file__).resolve().parent
SOURCE = FOLDER / "matrix.txt"
REPORT = FOLDER / "report.txt"


def read_positive_integer():
    """Повторяет ввод, пока не получено целое > 0. Различает типы ошибок."""
    while True:
        raw = input("Введите целое число больше нуля: ").strip()
        try:
            value = int(raw)
        except ValueError:
            print("Это не целое число, попробуйте снова")
            continue
        if value <= 0:
            print("Число должно быть больше нуля")
            continue
        return value


def format_line(label, values):
    return f"{label}: " + " ".join(str(v) for v in values)


def build_report(matrix):
    return [
        format_line("Суммы строк", row_sums(matrix)),
        format_line("Суммы столбцов", column_sums(matrix)),
        f"Результат варианта: {selected_sum(matrix)}",
    ]


def write_report(matrix):
    lines = build_report(matrix)
    with open(REPORT, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def main():
    print("== Проверка read_positive_integer ==")
    number = read_positive_integer()
    print(f"Принято число: {number}")

    # Вход открываем только на чтение. Отчёт записываем только после успеха.
    try:
        matrix = read_matrix(SOURCE)
    except FileNotFoundError:
        print(f"Файл не найден: {SOURCE}")
        return
    except UnicodeError:
        print("Не удалось прочитать файл в кодировке UTF-8")
        return
    except OSError as error:
        print(f"Ошибка доступа к файлу: {error}")
        return
    except ValueError as error:
        print(f"Некорректный формат данных: {error}")
        return

    try:
        write_report(matrix)
    except OSError as error:
        print(f"Не удалось записать отчёт: {error}")
        return

    for line in build_report(matrix):
        print(line)
    print("Отчёт записан:", REPORT)


if __name__ == "__main__":
    main()