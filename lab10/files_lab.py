def read_matrix(path):
    """Читает таблицу из файла. Формат: первая строка — rows columns, далее rows строк по columns чисел."""
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    if not content:
        raise ValueError("Файл пуст: отсутствует заголовок")

    # Допускается ровно один обычный перевод строки после последней строки данных.
    if content.endswith("\n"):
        content = content[:-1]

    lines = content.split("\n")

    header = lines[0].split()
    if len(header) != 2:
        raise ValueError("Строка 1: ожидалось два числа — количество строк и столбцов")

    try:
        rows, columns = int(header[0]), int(header[1])
    except ValueError:
        raise ValueError("Строка 1: ожидались целые числа в заголовке")

    if rows <= 0 or columns <= 0:
        raise ValueError("Строка 1: размеры должны быть положительными")

    data_lines = lines[1:]
    if len(data_lines) != rows:
        raise ValueError(
            f"Ожидалось {rows} строк данных, получено {len(data_lines)}"
        )

    matrix = []
    for index, raw_line in enumerate(data_lines):
        line_number = index + 2
        parts = raw_line.split()
        if len(parts) != columns:
            raise ValueError(
                f"Строка {line_number}: ожидалось {columns} чисел, получено {len(parts)}"
            )
        row = []
        for part in parts:
            try:
                row.append(int(part))
            except ValueError:
                raise ValueError(
                    f"Строка {line_number}: «{part}» не является целым числом"
                )
        matrix.append(row)
    return matrix


def selected_sum(matrix):
    """Вариант 8: сумма элементов первой строки. Пустая матрица → 0."""
    if not matrix:
        return 0
    return sum(matrix[0])