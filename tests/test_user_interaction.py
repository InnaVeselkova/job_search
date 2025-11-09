from unittest.mock import patch

from src.api_hh import HHVacanciesAPI
from src.user_interaction import user_interaction


# Тест без фильтрации и без диапазона зарплат
@patch('builtins.input', side_effect=[
    'Python',    # поисковый запрос
    '3',         # топ-N
    '',          # ключевые слова для фильтрации
    ''           # диапазон зарплаты
])
@patch.object(HHVacanciesAPI, 'get_vacancies')
def test_user_interaction_basic(mock_get_vacancies, mock_input):

    mock_get_vacancies.return_value = [
        {'name': 'Vac1', 'url': 'url1', 'salary': 100000, 'snippet': {'responsibility': 'desc1', 'requirement': 'req1'}, 'description': 'desc1'},
        {'name': 'Vac2', 'url': 'url2', 'salary': 150000, 'snippet': {'responsibility': 'desc2', 'requirement': 'req2'}, 'description': 'desc2'},
        {'name': 'Vac3', 'url': 'url3', 'salary': 90000, 'snippet': {'responsibility': 'desc3', 'requirement': 'req3'}, 'description': 'desc3'},
    ]

    result = user_interaction()

    # Проверка: вернулось 3 вакансии, отсортированные по убыванию зарплаты
    assert len(result) == 3
    assert result[0].name == 'Vac2'
    assert result[1].name == 'Vac1'
    assert result[2].name == 'Vac3'


# Тест с фильтрацией по ключевым словам, диапазоном зарплат и ограничением top N
@patch('builtins.input', side_effect=[
    'Data Scientist',  # поисковый запрос
    '2',               # топ N
    'python',       # ключевые слова
    '80000-200000'     # диапазон зарплат
])
@patch.object(HHVacanciesAPI, 'get_vacancies')
def test_user_interaction_with_filters(mock_get_vacancies, mock_input):
    mock_get_vacancies.return_value = [
        {'name': 'VacA', 'url': 'urlA', 'salary': 90000, 'snippet': {'responsibility': 'descA', 'requirement': 'reqA'}, 'description': 'Python'},
        {'name': 'VacB', 'url': 'urlB', 'salary': 150000, 'snippet': {'responsibility': 'descB', 'requirement': 'reqB'}, 'description': 'AI'},
        {'name': 'VacC', 'url': 'urlC', 'salary': 70000, 'snippet': {'responsibility': 'descC', 'requirement': 'reqC'}, 'description': 'Java'},
    ]

    result = user_interaction()

    assert len(result) == 1
    assert any(v.name == 'VacA' for v in result)
    assert all(v._get_salary_value() >= 80000 and v._get_salary_value() <= 200000 for v in result)


# Тест с некорректным вводом для N
@patch('builtins.input', side_effect=[
    'Test',      # поисковый запрос
    'abc',       # некорректный ввод
    '',          # ключевые слова
    ''           # диапазон
])
@patch.object(HHVacanciesAPI, 'get_vacancies')
def test_user_interaction_invalid_topN(mock_get_vacancies, mock_input):
    mock_get_vacancies.return_value = [
        {'name': 'TestVac', 'url': 'url', 'salary': 50000, 'snippet': {'responsibility': 'desc', 'requirement': 'req'}, 'description': 'desc'}
    ]

    result = user_interaction()
    # По умолчанию должно взять top_n=5
    assert len(result) == 1
    assert result[0].name == 'TestVac'
