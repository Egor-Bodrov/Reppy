import json

from analysis import (
    validate_todos,
    completion_counts,
    top_users,
    select_tasks,
)


TUTORIAL = [
    {"id": 1, "userId": 5, "title": "Ввод", "completed": True},
    {"id": 2, "userId": 5, "title": "Циклы", "completed": False},
    {"id": 3, "userId": 10, "title": "Строки", "completed": True},
    {"id": 4, "userId": 10, "title": "Файлы", "completed": True},
    {"id": 5, "userId": 5, "title": "Списки", "completed": True},
]


def expect_value_error(call, comment):
    try:
        call()
    except ValueError:
        return
    else:
        assert False, f"ValueError не был выброшен: {comment}"


def test_validate_ok():
    assert validate_todos(TUTORIAL) is TUTORIAL
    assert validate_todos([]) == []


def test_validate_errors():
    expect_value_error(lambda: validate_todos({"id": 1}), "корень не список")
    expect_value_error(lambda: validate_todos([42]), "элемент не объект")
    expect_value_error(
        lambda: validate_todos([{"id": 1, "title": "x", "completed": True}]),
        "нет userId",
    )
    expect_value_error(
        lambda: validate_todos([{"id": 1, "userId": 5, "title": "x",
                                 "completed": "false"}]),
        "completed не bool",
    )
    expect_value_error(
        lambda: validate_todos([{"id": True, "userId": 5, "title": "x",
                                 "completed": True}]),
        "id=True не считается целым",
    )
    expect_value_error(
        lambda: validate_todos([
            {"id": 1, "userId": 5, "title": "x", "completed": True},
            {"id": 1, "userId": 5, "title": "y", "completed": False},
        ]),
        "повторный id",
    )
    expect_value_error(
        lambda: validate_todos([{"id": 0, "userId": 5, "title": "x",
                                 "completed": True}]),
        "id не положительный",
    )


def test_completion_counts_and_top():
    assert completion_counts(TUTORIAL) == {5: 2, 10: 2}
    assert top_users({5: 2, 10: 2}) == [5, 10]
    assert top_users({}) == []
    assert top_users({5: 0, 10: 0}) == []
    assert top_users({5: 3, 10: 1}) == [5]


def test_select_variant8():
    # Идентификаторы по таблице для user_id=5, подстрока "и"
    result = select_tasks(TUTORIAL, 5, "и")
    assert [todo["id"] for todo in result] == [2, 5]

    # Поиск без учёта регистра
    upper = select_tasks(TUTORIAL, 5, "И")
    assert [todo["id"] for todo in upper] == [2, 5]

    # Смешанный регистр и другая подстрока
    mixed = select_tasks(TUTORIAL, 5, "СпИ")
    assert [todo["id"] for todo in mixed] == [5]

    # Неизвестный пользователь → []
    assert select_tasks(TUTORIAL, 999, "и") == []

    # Нет совпадений по подстроке → []
    assert select_tasks(TUTORIAL, 5, "zzz") == []

    # Исходный набор не изменён
    saved = [todo.copy() for todo in TUTORIAL]
    select_tasks(TUTORIAL, 5, "и")
    assert TUTORIAL == saved


def test_leaders_selection():
    leaders = top_users(completion_counts(TUTORIAL))
    leader_ids = set(leaders)
    tasks = [
        todo for todo in TUTORIAL
        if todo["userId"] in leader_ids and todo["completed"]
    ]
    assert [todo["id"] for todo in tasks] == [1, 3, 4, 5]


def test_json_roundtrip():
    selected = select_tasks(TUTORIAL, 5, "и")
    text = json.dumps(selected, ensure_ascii=False)
    assert json.loads(text) == selected


def run_all():
    test_validate_ok()
    test_validate_errors()
    test_completion_counts_and_top()
    test_select_variant8()
    test_leaders_selection()
    test_json_roundtrip()


if __name__ == "__main__":
    run_all()
    print("Все проверки пройдены.")