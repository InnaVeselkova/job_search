class Vacancy:
    __slots__ = ['name', 'url', 'salary', 'description']

    def __init__(self, name, url, salary, description):
        self._validate_name(name)
        self._validate_url(url)
        self._validate_salary(salary)
        self._validate_description(description)

        self.name = name
        self.url = url
        self.salary = salary
        self.description = description

    # Магические методы сравнения по зарплате
    def __lt__(self, other):
        return self._get_salary_value() < other._get_salary_value()

    def __eq__(self, other):
        return self._get_salary_value() == other._get_salary_value()

    def parse_vacancies(vac_dicts):
        vacancies = []
        for v in vac_dicts:
            name = v.get('name', 'Без названия')
            url = v.get('alternate_url') or v.get('url', '')
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

    # Приватные методы валидации
    def _validate_name(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError("Неверный формат названия вакансии.")

    def _validate_url(self, url):
        if not isinstance(url, str) or not url.startswith('http'):
            raise ValueError("Некорректная ссылка на вакансию.")

    def _validate_salary(self, salary):
        if not (isinstance(salary, (dict, str, int, float))):
            raise ValueError("Неверный формат зарплаты.")

    def _validate_description(self, description):
        if not isinstance(description, str):
            raise ValueError("Описание должно быть строкой.")


def parse_vacancies(vac_dict):
    """Функция для преобразования списка словарей в список объектов Vacancy"""
    vacancies = []
    for v in vac_dict:
        name = v.get('name', 'Без названия')
        url = v.get('alternate_url') or v.get('url', '')
        salary = v.get('salary')
        description = v.get('snippet', {}).get('responsibility', '')
        requirements = v.get('snippet', {}).get('requirement', '')
        vacancy_obj = Vacancy(name, url, salary, description, requirements)
        vacancies.append(vacancy_obj)
    return vacancies