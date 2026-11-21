from logic import (
    add_record,
    delete_record,
    find_records,
    next_id,
    set_completed,
    statistics,
    validate_records,
)


SAMPLE = [
    {"id": 1, "title": "Перевал Карпатский", "category": "горный", "amount": 18, "completed": True},
    {"id": 2, "title": "Тропа Шевченко", "category": "лесной", "amount": 12, "completed": False},
    {"id": 3, "title": "Центр Киева", "category": "городской", "amount": 5, "completed": True},
]


def copy_sample():
    return [record.copy() for record in SAMPLE]


def expect_value_error(call, comment):
    try:
        call()
    except ValueError:
        return
    else:
        assert False, f"ValueError не был выброшен: {comment}"


def test_validate_ok():
    assert validate_records(copy_sample()) is not None
    assert validate_records([]) == []


def test_validate_errors():
    expect_value_error(lambda: validate_records({"id": 1}), "корень не список")
    expect_value_error(lambda: validate_records([42]), "элемент не объект")
    expect_value_error(
        lambda: validate_records([
            {"id": 1, "title": "a", "category": "b", "amount": 1,
             "completed": True},
            {"id": 1, "title": "c", "category": "d", "amount": 2,
             "completed": False},
        ]),
        "повторный id",
    )
    expect_value_error(
        lambda: validate_records([
            {"id": 1, "title": "a", "category": "b", "amount": True,
             "completed": True},
        ]),
        "amount=True не считается числом",
    )
    expect_value_error(
        lambda: validate_records([
            {"id": 1, "title": "a", "category": "b", "amount": -1,
             "completed": True},
        ]),
        "отрицательный amount",
    )
    expect_value_error(
        lambda: validate_records([
            {"id": 1, "title": "a", "category": "b", "amount": 1,
             "completed": "true"},
        ]),
        "completed строкой",
    )
    expect_value_error(
        lambda: validate_records([
            {"id": 1, "title": "   ", "category": "b", "amount": 1,
             "completed": True},
        ]),
        "пустой title после strip",
    )


def test_next_id():
    assert next_id([]) == 1
    assert next_id([{"id": 5}]) == 6
    assert next_id([{"id": 2}, {"id": 9}]) == 10


def test_add_record():
    records = copy_sample()
    record = add_record(records, "  Новый маршрут  ", "  горный  ", 10)
    assert record == {
        "id": 4,
        "title": "Новый маршрут",
        "category": "горный",
        "amount": 10,
        "completed": False,
    }
    assert records[-1] is record
    expect_value_error(lambda: add_record(records, "  ", "x", 1), "пустой title")
    expect_value_error(lambda: add_record(records, "a", " ", 1), "пустая category")
    expect_value_error(lambda: add_record(records, "a", "b", -1), "amount < 0")


def test_find_records():
    records = copy_sample()
    assert [r["id"] for r in find_records(records, "ПЕРЕВАЛ")] == [1]
    assert [r["id"] for r in find_records(records, "тропа")] == [2]
    assert find_records(records, "zzz") == []
    expect_value_error(lambda: find_records(records, "   "), "пустой запрос")
    assert records == SAMPLE


def test_set_completed():
    records = copy_sample()
    assert set_completed(records, 2, True) is True
    assert records[1]["completed"] is True
    assert set_completed(records, 999, True) is False
    expect_value_error(lambda: set_completed(records, 1, "yes"), "completed строкой")


def test_delete_record():
    records = [
        {"id": 1, "title": "a", "category": "b", "amount": 1, "completed": False},
        {"id": 2, "title": "c", "category": "d", "amount": 2, "completed": True},
    ]
    assert delete_record(records, 1) is True
    assert [r["id"] for r in records] == [2]
    assert next_id(records) == 3
    assert delete_record(records, 999) is False


def test_statistics():
    records = copy_sample()
    stats = statistics(records)
    assert stats["total"] == 3
    assert stats["completed"] == 2
    assert stats["not_completed"] == 1
    assert stats["amount_sum"] == 35
    assert stats["by_category"] == {"горный": 18, "лесной": 12, "городской": 5}
    assert records == SAMPLE


def test_statistics_empty():
    stats = statistics([])
    assert stats == {
        "total": 0,
        "completed": 0,
        "not_completed": 0,
        "amount_sum": 0,
        "by_category": {},
    }


def test_duplicate_titles():
    records = [
        {"id": 1, "title": "Same", "category": "x", "amount": 1, "completed": False},
        {"id": 2, "title": "Same", "category": "y", "amount": 2, "completed": True},
    ]
    assert [r["id"] for r in find_records(records, "same")] == [1, 2]


def run_all():
    test_validate_ok()
    test_validate_errors()
    test_next_id()
    test_add_record()
    test_find_records()
    test_set_completed()
    test_delete_record()
    test_statistics()
    test_statistics_empty()
    test_duplicate_titles()


if __name__ == "__main__":
    run_all()
    print("Все проверки logic пройдены.")