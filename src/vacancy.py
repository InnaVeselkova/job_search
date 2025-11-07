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
