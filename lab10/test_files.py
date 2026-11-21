from pathlib import Path
from tempfile import TemporaryDirectory

from files_lab import read_matrix, selected_sum


def write_and_read(text):
    with TemporaryDirectory() as directory:
        path = Path(directory) / "matrix.txt"
        path.write_text(text, encoding="utf-8")
        return read_matrix(path)


def expect_value_error(text, comment):
    try:
        write_and_read(text)
    except ValueError:
        return
    else:
        assert False, f"Ошибка не обнаружена: {comment}"


def test_read_ok():
    assert write_and_read("1 2\n7 -1\n") == [[7, -1]]
    assert write_and_read("1 1\n0\n") == [[0]]
    # Один обычный перевод строки после последней строки допустим
    assert write_and_read("2 3\n1 -2 3\n4 0 -6\n") == [[1, -2, 3], [4, 0, -6]]


def test_read_errors():
    expect_value_error("", "пустой файл")
    expect_value_error("0 3\n1 2 3\n", "заголовок 0 3")
    expect_value_error("1 2\n1\n", "строка 1 вместо двух чисел")
    expect_value_error("1 2\n1 x\n", "нечисловая ячейка")
    expect_value_error("1 1\n1\n2\n", "лишняя строка данных")
    expect_value_error("1 1\n1\n\n", "пустая строка после данных")


def test_missing_file():
    missing = Path("/this/path/should/not/exist/matrix.txt")
    try:
        read_matrix(missing)
    except FileNotFoundError:
        return
    assert False, "FileNotFoundError не был выброшен"


def test_selected_sum_variant8():
    assert selected_sum([[1, -2, 3], [4, 0, -6]]) == 2
    assert selected_sum([[7]]) == 7          # 1×1: первая строка — единственная
    assert selected_sum([[0, 0], [5, 5]]) == 0
    assert selected_sum([]) == 0


def test_read_does_not_modify_input_file():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "matrix.txt"
        original = "2 3\n1 -2 3\n4 0 -6\n"
        path.write_text(original, encoding="utf-8")
        read_matrix(path)
        assert path.read_text(encoding="utf-8") == original


def run_all():
    test_read_ok()
    test_read_errors()
    test_missing_file()
    test_selected_sum_variant8()
    test_read_does_not_modify_input_file()


if __name__ == "__main__":
    run_all()
    print("Все проверки пройдены.")