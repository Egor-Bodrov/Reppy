from collections_lab import (
    word_counts,
    sorted_word_counts,
    common_topics,
    all_topics,
    totals_by_category,
    titles_in_category,
)


# Вариант 8: туристические маршруты, amount — километры.
RECORDS = [
    {"title": "Перевал Карпатский", "category": "горный", "amount": 18},
    {"title": "Тропа Шевченко",    "category": "лесной", "amount": 12},
    {"title": "Центр Киева",       "category": "городской", "amount": 5},
    {"title": "Хребет Свидовец",   "category": "горный", "amount": 25},
    {"title": "Уманский парк",     "category": "лесной", "amount": 7},
    {"title": "Львовская ратуша",  "category": "городской", "amount": 3},
]


def demo_words():
    text = "Python, python! SQL; git: git."
    counts = word_counts(text)
    print("Текст:", text)
    for word, count in sorted_word_counts(counts):
        print(f"  {word}: {count}")


def demo_topics():
    first = ["python", "sql", "python"]
    second = ["sql", "git"]
    print("Общие темы:", common_topics(first, second))
    print("Все темы:  ", all_topics(first, second))


def demo_record():
    record = {"title": "Перевал Карпатский", "hours": 4}
    record["hours"] = 5
    record["completed"] = False

    pair = (record["title"], record["hours"])
    name, hours = pair
    print("Запись:", record)
    print(f"Пара: {name}, {hours}")


def demo_variant():
    totals = totals_by_category(RECORDS)
    print("Сводка по категориям:")
    for category in sorted(totals):
        print(f"  {category}: {totals[category]} км")

    requested = input("Введите категорию для поиска: ").strip()
    print("Найденные маршруты:", titles_in_category(RECORDS, requested))


def main():
    print("== Частоты слов ==")
    demo_words()
    print("\n== Учебные интересы ==")
    demo_topics()
    print("\n== Запись и пара ==")
    demo_record()
    print("\n== Вариант 8: туристические маршруты ==")
    demo_variant()


if __name__ == "__main__":
    main()