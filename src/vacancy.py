from src.api_hh import HHVacanciesAPI
from src.parsers import parse_vacancies


class Vacancy:
    __slots__ = ['name', 'url', 'salary', 'description', 'requirements']

    def __init__(self, name, url, salary, description, requirements=''):

        self._validate_salary(salary)

        self.name = name
        self.url = url
        self.salary = salary
        self.description = description
        self.requirements = requirements

    def __str__(self):
        return (
            f"Вакансия: {self.name}\n"
            f"Зарплата: {self._get_salary_value()}\n"
            f"Ссылка: {self.url}\n"
            f"Описание: {self.description}\n"
            f"Требования: {self.requirements}\n"
            "------------------------"
        )

    # Магические методы сравнения по зарплате
    def __lt__(self, other):
        return self._get_salary_value() < other._get_salary_value()

    def __eq__(self, other):
        return self._get_salary_value() == other._get_salary_value()

    def parse_vacancies(vac_dicts):
        vacancies = []
        for v in vac_dicts:
            name = v.get('name', 'Без названия')
            url = v.get('url', '')
            salary = v.get('salary')
            description = v.get('snippet', {}).get('responsibility', '')
            requirements = v.get('snippet', {}).get('requirement', '')
            vacancy_obj = Vacancy(name, url, salary, description, requirements)
            vacancies.append(vacancy_obj)
        return vacancies

    # Приватный метод для получения числового значения зарплаты
    def _get_salary_value(self):
        if isinstance(self.salary, dict):
            if self.salary.get('from'):
                return self.salary.get('from')
            elif self.salary.get('to'):
                return self.salary.get('to')
        elif isinstance(self.salary, str):
            if self.salary == 'Зарплата не указана':
                return 0
        elif isinstance(self.salary, (int, float)):
            return self.salary
        return 0

    def _validate_salary(self, salary):
        if salary is None:
            self.salary = 'Зарплата не указана'
        elif not isinstance(salary, (dict, str, int, float)):
            raise ValueError("Неверный формат зарплаты.")
        else:
            self.salary = salary


if __name__ == "__main__":
    api = HHVacanciesAPI()
    keyword = "python разработчик"
    vacs_dicts = api.get_vacancies(keyword)
    vacancies = parse_vacancies(vacs_dicts)
    print(f"Найдено {len(vacancies)} вакансий по запросу '{keyword}':")
    sorted_vacancies = sorted(vacancies, reverse=True, key=lambda v: v._get_salary_value())
    for v in sorted_vacancies[:5]:
        print(f"Вакансия: {v.name}")
        print(f"Ссылка: {v.url}")
        print(f"Зарплата: {v.salary}")
