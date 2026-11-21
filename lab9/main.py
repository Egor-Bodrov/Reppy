from table import row_sums, column_sums, diagonal_pattern, transform


def read_matrix():
    rows = int(input("Количество строк: "))
    columns = int(input("Количество столбцов: "))
    matrix = []
    for index in range(rows):
        row = [int(part) for part in input(f"Строка {index + 1}: ").split()]
        while len(row) != columns:
            print(f"Нужно ровно {columns} чисел")
            row = [int(part) for part in input("Повторите строку: ").split()]
        matrix.append(row)
    return matrix


def print_matrix(title, matrix):
    print(title)
    for row in matrix:
        print("  ", *row)


def main():
    matrix = read_matrix()
    print_matrix("Исходная таблица:", matrix)
    print("Суммы строк:   ", row_sums(matrix))
    print("Суммы столбцов:", column_sums(matrix))

    size = int(input("Положительный размер узора: "))
    while size < 1:
        size = int(input("Размер должен быть >= 1, повторите: "))
    print_matrix("Диагональный узор:", diagonal_pattern(size))

    new_matrix = transform(matrix)
    print_matrix("После transform (вариант 8):", new_matrix)

    # Демонстрация: результат независим от исходной матрицы
    if new_matrix:
        new_matrix[0][0] = 999
        print("Исходная после правки копии:", matrix[0][0])


if __name__ == "__main__":
    main()