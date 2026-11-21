from collections_lab import (
    word_counts,
    sorted_word_counts,
    common_topics,
    all_topics,
    totals_by_category,
    titles_in_category,
)


EXAMPLE = [
    {"title": "A", "category": "основное", "amount": 4},
    {"title": "B", "category": "дополнительное", "amount": 2},
    {"title": "C", "category": "основное", "amount": 3},
]


def test_word_counts():
    assert word_counts("Python, python! SQL") == {"python": 2, "sql": 1}
    assert word_counts("!!!") == {}
    assert word_counts("") == {}
    assert word_counts("A... B, C! C; C:") == {"a": 1, "b": 1, "c": 3}


def test_sorted_word_counts():
    assert sorted_word_counts({"sql": 1, "python": 2}) == [("python", 2), ("sql", 1)]


def test_topics():
    first = ["python", "sql", "python"]
    second = ["sql", "git"]
    assert common_topics(first, second) == ["sql"]
    assert all_topics(first, second) == ["git", "python", "sql"]

    assert common_topics([], ["a", "b"]) == []
    assert all_topics([], ["a", "b"]) == ["a", "b"]
    assert all_topics(["a", "a"], []) == ["a"]


def test_totals_by_category():
    assert totals_by_category(EXAMPLE) == {"основное": 7, "дополнительное": 2}
    assert totals_by_category([]) == {}


def test_titles_in_category():
    assert titles_in_category(EXAMPLE, "основное") == ["A", "C"]
    assert titles_in_category(EXAMPLE, "нет") == []


def test_records_not_modified():
    saved = [record.copy() for record in EXAMPLE]
    totals_by_category(EXAMPLE)
    titles_in_category(EXAMPLE, "основное")
    assert EXAMPLE == saved


def run_all():
    test_word_counts()
    test_sorted_word_counts()
    test_topics()
    test_totals_by_category()
    test_titles_in_category()
    test_records_not_modified()


if __name__ == "__main__":
    run_all()
    print("Все проверки пройдены.")