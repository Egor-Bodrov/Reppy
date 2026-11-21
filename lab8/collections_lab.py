PUNCTUATION = ".,!?;:"


def word_counts(text):
    """Словарь «слово → количество». Регистр не важен, краевая пунктуация срезается."""
    counts = {}
    for raw in text.lower().split():
        word = raw.strip(PUNCTUATION)
        if not word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts


def sorted_word_counts(counts):
    """Пары (слово, количество) по алфавиту — для детерминированного вывода."""
    return [(word, counts[word]) for word in sorted(counts)]


def common_topics(first, second):
    """Отсортированный список общих тем."""
    return sorted(set(first) & set(second))


def all_topics(first, second):
    """Отсортированный список всех уникальных тем."""
    return sorted(set(first) | set(second))


def totals_by_category(records):
    """Словарь сумм amount по категориям. Входные записи не меняются."""
    totals = {}
    for record in records:
        category = record["category"]
        totals[category] = totals.get(category, 0) + record["amount"]
    return totals


def titles_in_category(records, category):
    """Названия записей указанной категории в исходном порядке."""
    return [record["title"] for record in records if record["category"] == category]