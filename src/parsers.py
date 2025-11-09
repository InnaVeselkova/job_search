from typing import List, Dict

from src.vacancy import Vacancy


def parse_vacancies(vac_dict: List[Dict[str, any]]) -> List['Vacancy']:
    """
    Функция для преобразования списка вакансий в список объектов Vacancy
    """
    vacancies = []
    for v in vac_dict:
        name = v.get('name', 'Без названия')
        url = v.get('url', '')
        salary = v.get('salary')
        description = v.get('snippet', {}).get('responsibility', '')
        requirements = v.get('snippet', {}).get('requirement', '')
        vacancy_obj = Vacancy(name, url, salary, description, requirements)
        vacancies.append(vacancy_obj)
    return vacancies
