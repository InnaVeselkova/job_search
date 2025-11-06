import json
from abc import ABC, abstractmethod

from src.api_hh import HHVacanciesAPI
from src.vacancy import Vacancy
from src.parsers import parse_vacancies


class FileHandler(ABC):
    @abstractmethod
    def add_data(self, data):
        pass

    @abstractmethod
    def get_data(self, filter_func=None):
        pass

    @abstractmethod
    def delete_data(self, criteria):
        pass


class JSONFileHandler(FileHandler):
    def __init__(self, filename='vacancies.json'):
        self.__filename = filename
        self._load()

    def _load(self):
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
                self._remove_duplicates()
        except FileNotFoundError:
            self._data = []

    def _save(self):
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4)

    def _remove_duplicates(self):
        seen = set()
        unique_data = []
        for item in self._data:
            item_str = json.dumps(item, sort_keys=True)
            if item_str not in seen:
                seen.add(item_str)
                unique_data.append(item)
        self._data = unique_data

    def add_data(self, vacancy: 'Vacancy'):
        # Добавляет уникальную вакансию; избегая дубли
        vac_dict = {
            'name': vacancy.name,
            'url': vacancy.url,
            'salary': vacancy.salary,
            'description': vacancy.description,
            'requirements': vacancy.requirements
        }
        if vac_dict not in self._data:
            self._data.append(vac_dict)
            self._save()

    def get_data(self, filter_func=None):
        if filter_func is None:
            return self._data
        return list(filter(filter_func, self._data))

    def delete_data(self, criteria):
        self._data = list(filter(lambda v: not criteria(v), self._data))
        self._save()


if __name__ == "__main__":
    api = HHVacanciesAPI()
    keyword = "python разработчик"
    vacs_dicts = api.get_vacancies(keyword)
    vacancies = parse_vacancies(vacs_dicts)
    print(f"Найдено {len(vacancies)} вакансий по запросу '{keyword}':")
    sorted_vacancies = sorted(vacancies, reverse=True, key=lambda v: v._get_salary_value())

    # Инициализация обработчика файла
    file_handler = JSONFileHandler()

    print("Топ 5 вакансий и их сохранение в файл:")
    for v in sorted_vacancies[:5]:
        print(f"Вакансия: {v.name}")
        print(f"Ссылка: {v.url}")
        print(f"Зарплата: {v.salary}")
        print(f"Описание: {v.description}")
        # Создаем объект и сохраняем
        vacancy_obj = Vacancy(
            v.name, v.url, v.salary, v.description, v.requirements
        )
        file_handler.add_data(vacancy_obj)

    # Получение всех вакансий из файла
    print("\nВсе вакансии из файла:")
    for v in file_handler.get_data():
        print(v)
