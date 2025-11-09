from src.parsers import parse_vacancies


def test_parse_vacancies_basic():
    vac_list = [
        {
            'name': 'Frontend Developer',
            'url': 'http://example.com/1',
            'salary': 120000,
            'snippet': {
                'responsibility': 'Develop UI',
                'requirement': 'React, JS'
            }
        },
        {
            'name': 'Backend Developer',
            'url': 'http://example.com/2',
            'salary': {'from': 100000},
            'snippet': {
                'responsibility': 'Develop API',
                'requirement': 'Python, Django'
            }
        }
    ]

    vacancies = parse_vacancies(vac_list)

    assert len(vacancies) == 2
    assert vacancies[0].name == 'Frontend Developer'
    assert vacancies[0].url == 'http://example.com/1'
    assert vacancies[0].salary == 120000
    assert 'UI' in str(vacancies[0])

    assert vacancies[1].name == 'Backend Developer'
    assert vacancies[1].salary == {'from': 100000}
    assert 'API' in str(vacancies[1])


def test_parse_vacancies_missing_fields():
    vac_list = [
        {
            # пропущено 'name'
            'url': 'http://example.com/3',
            'salary': 'Зарплата не указана',
            'snippet': {
                'responsibility': 'Some responsibility'
                # пропущено 'requirement'
            }
        }
    ]
    vacancies = parse_vacancies(vac_list)
    assert len(vacancies) == 1
    v = vacancies[0]
    assert v.name == 'Без названия'
    assert v.url == 'http://example.com/3'
    assert v.salary == 'Зарплата не указана'
    assert 'responsibility' in str(v)


def test_parse_vacancies_empty():
    result = parse_vacancies([])
    assert result == []


def test_parse_vacancies_with_none():
    vac_list = [
        {
            'name': None,
            'url': None,
            'salary': None,
            'snippet': {}
        }
    ]
    vacancies = parse_vacancies(vac_list)
    assert len(vacancies) == 1
    v = vacancies[0]
    assert v.name is None
    assert v.url is None
    assert v.salary is None
