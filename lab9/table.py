def row_sums(matrix):
    """Суммы строк. Для [] возвращает []."""
    return [sum(row) for row in matrix]


def column_sums(matrix):
    """Суммы столбцов. Матрица непустая и прямоугольная, столбцов >= 1."""
    if not matrix:
        return []
    columns = len(matrix[0])
    return [sum(row[column] for row in matrix) for column in range(columns)]


def diagonal_pattern(size):
    """Квадрат size×size: диагональ 0, выше 1, ниже 2."""
    return [
        [0 if row == column else 1 if row < column else 2
         for column in range(size)]
        for row in range(size)
    ]


def transform(matrix):
    """Вариант 8: отрицательные элементы уменьшить на 2, остальные оставить."""
    return [
        [number - 2 if number < 0 else number for number in row]
        for row in matrix
    ]