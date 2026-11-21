from table import row_sums, column_sums, diagonal_pattern, transform


def test_row_sums():
    assert row_sums([[1, 2, 3], [4, 5, 6]]) == [6, 15]
    assert row_sums([[7]]) == [7]
    assert row_sums([[1], [-1], [0]]) == [1, -1, 0]
    assert row_sums([]) == []


def test_column_sums():
    assert column_sums([[1, 2, 3], [4, 5, 6]]) == [5, 7, 9]
    assert column_sums([[7]]) == [7]
    assert column_sums([[1], [-1], [0]]) == [0]
    assert column_sums([]) == []


def test_diagonal_pattern():
    assert diagonal_pattern(1) == [[0]]
    assert diagonal_pattern(3) == [
        [0, 1, 1],
        [2, 0, 1],
        [2, 2, 0],
    ]


def test_transform_variant8():
    assert transform([[-2, 0, 3], [4, -5, 6]]) == [[-4, 0, 3], [4, -7, 6]]
    assert transform([]) == []


def test_transform_does_not_modify_source():
    source = [[-2, 0, 3], [4, -5, 6]]
    saved = [row.copy() for row in source]

    result = transform(source)
    result[0][0] = 100

    assert source == saved  # исходная матрица не изменилась


def test_row_sums_not_modified():
    source = [[1, 2, 3], [4, 5, 6]]
    saved = [row.copy() for row in source]
    row_sums(source)
    column_sums(source)
    assert source == saved


def run_all():
    test_row_sums()
    test_column_sums()
    test_diagonal_pattern()
    test_transform_variant8()
    test_transform_does_not_modify_source()
    test_row_sums_not_modified()


if __name__ == "__main__":
    run_all()
    print("Все проверки пройдены.")