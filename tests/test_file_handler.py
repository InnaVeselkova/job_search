import json

import pytest

from src.file_handler import JSONFileHandler
from src.vacancy import Vacancy


@pytest.fixture
def temp_json_file(tmp_path):
    filename = tmp_path / "test_vacancies.json"
    yield filename


def test_load_existing_data(tmp_path):
    data = [
        {"name": "Vac1", "url": "http://", "salary": 50000, "description": "desc", "requirements": "req"}
    ]
    filename = tmp_path / "data.json"
    filename.write_text(json.dumps(data))
    handler = JSONFileHandler(str(filename))
    assert handler._data == data


def test_add_data_and_save(tmp_path):
    filename = tmp_path / "save.json"
    handler = JSONFileHandler(str(filename))
    handler._data = []  # чистим
    vacancy = Vacancy("Test", "http://", 100000, "desc", "req")
    handler.add_data(vacancy)
    assert any(d['name'] == "Test" for d in handler._data)
    # Проверяем сохранение в файл
    data_in_file = json.loads(filename.read_text())
    assert data_in_file[0]['name'] == "Test"


def test_remove_duplicates(tmp_path):
    filename = tmp_path / "dupes.json"
    data = [
        {"name": "Vac1", "url": "", "salary": 0, "description": "", "requirements": ""},
        {"name": "Vac1", "url": "", "salary": 0, "description": "", "requirements": ""}  # дубликат
    ]
    filename.write_text(json.dumps(data))
    handler = JSONFileHandler(str(filename))
    handler._remove_duplicates()
    assert len(handler._data) == 1


def test_get_data_filter(tmp_path):
    filename = tmp_path / "filter.json"
    handler = JSONFileHandler(str(filename))
    handler._data = [
        {"name": "Vac1", "salary": 100},
        {"name": "Vac2", "salary": 200}
    ]
    result = handler.get_data(filter_func=lambda v: v['salary'] > 150)
    assert len(result) == 1
    assert result[0]['name'] == "Vac2"


def test_delete_data(tmp_path):
    filename = tmp_path / "delete.json"
    handler = JSONFileHandler(str(filename))
    handler._data = [
        {"name": "Vac1", "salary": 100},
        {"name": "Vac2", "salary": 200}
    ]
    handler.delete_data(lambda v: v['name'] == "Vac1")
    assert len(handler._data) == 1
    assert handler._data[0]['name'] == "Vac2"
    # Проверка сохранения
    data_in_file = json.loads(filename.read_text())
    assert data_in_file[0]['name'] == "Vac2"


def test_integration_end_to_end(tmp_path):
    filename = tmp_path / "full.json"
    handler = JSONFileHandler(str(filename))
    handler._data = []

    # Создаем вакансии
    v1 = Vacancy("Vac1", "url1", 1000, "desc1")
    v2 = Vacancy("Vac2", "url2", 2000, "desc2")
    handler.add_data(v1)
    handler.add_data(v2)
    # Проверка, что обе добавлены
    assert len(handler._data) == 2

    # Удаляем одну
    handler.delete_data(lambda v: v['name'] == "Vac1")
    assert len(handler._data) == 1
    assert handler._data[0]['name'] == "Vac2"

    # Получение данных
    all_data = handler.get_data()
    assert isinstance(all_data, list)
    assert all_data[0]['name'] == "Vac2"
