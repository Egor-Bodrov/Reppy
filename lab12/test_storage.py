import json
from pathlib import Path
from tempfile import TemporaryDirectory

from storage import load_records, save_records


SAMPLE = [
    {"id": 1, "title": "Перевал Карпатский", "category": "горный", "amount": 18, "completed": True},
    {"id": 2, "title": "Тропа Шевченко", "category": "лесной", "amount": 12, "completed": False},
]


def test_roundtrip():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        save_records(path, SAMPLE)
        loaded = load_records(path)
        assert loaded == SAMPLE


def test_missing_file():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "nope.json"
        try:
            load_records(path)
        except FileNotFoundError:
            return
        assert False, "FileNotFoundError не был выброшен"


def test_broken_json_not_overwritten():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        broken = "{not a json"
        path.write_text(broken, encoding="utf-8")
        try:
            load_records(path)
        except ValueError:
            pass
        else:
            assert False, "Ошибка JSON не обнаружена"
        assert path.read_text(encoding="utf-8") == broken


def test_bad_structure():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        path.write_text(json.dumps([{"id": 1}]), encoding="utf-8")
        try:
            load_records(path)
        except ValueError:
            return
        assert False, "Ошибка структуры не обнаружена"


def run_all():
    test_roundtrip()
    test_missing_file()
    test_broken_json_not_overwritten()
    test_bad_structure()


if __name__ == "__main__":
    run_all()
    print("Все проверки storage пройдены.")