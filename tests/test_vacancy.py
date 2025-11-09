from src.vacancy import Vacancy


def test_creation_with_int_salary():
    v = Vacancy("Developer", "http://link", 100000, "Dev description")
    assert v.name == "Developer"
    assert v.salary == 100000
    assert v._get_salary_value() == 100000


def test_creation_with_str_salary():
    v = Vacancy("Seeker", "http://link", "Зарплата не указана", "desc")
    assert v._get_salary_value() == 0


def test_creation_with_dict_from():
    salary = {'from': 50000}
    v = Vacancy("Analyst", "http://link", salary, "desc")
    assert v._get_salary_value() == 50000


def test_creation_with_dict_to():
    salary = {'to': 30000}
    v = Vacancy("Tester", "http://link", salary, "desc")
    assert v._get_salary_value() == 30000


def test_str_representation():
    salary = {'from': 50000}
    v = Vacancy("Manager", "http://link", salary, "desc", "requirements")
    s = str(v)
    assert "Вакансия: Manager" in s
    assert "Зарплата: 50000" in s
    assert "Ссылка: http://link" in s
    assert "Описание: desc" in s
    assert "Требования: requirements" in s
    assert s.endswith("------------------------")


def test_comparison_lt():
    v1 = Vacancy("V1", "url1", 100, "desc")
    v2 = Vacancy("V2", "url2", 200, "desc")
    assert v1 < v2
    assert not v2 < v1


def test_comparison_eq():
    Vacancy("V1", "url1", 100, "desc")
    Vacancy("V2", "url2", 100, "desc")
