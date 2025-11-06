import requests
from abc import ABC, abstractmethod
import time


class VacanciesAPI(ABC):
    @abstractmethod
    def _connect(self):
        """Приватный метод проверки соединения с API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """Получить список вакансий по ключевому слову."""
        pass


class HHVacanciesAPI(VacanciesAPI):
    def __init__(self):
        self.__base_url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'MyVacancyApp'}
        self._connect()

    def _connect(self):
        response = requests.get(self.__base_url)
        if response.status_code == 200:
            print("Подключение успешно к hh.ru")
        else:
            raise ConnectionError(f"Ошибка подключения: {response.status_code}")

    def get_vacancies(self, keyword: str):
        params = {
            'text': keyword,
            'per_page': 100,
            'page': 0
        }
        all_vacancies = []

        while True:
            self._connect()

            response = requests.get(self.__base_url, headers=self.__headers, params=params)
            if response.status_code != 200:
                print(f"Ошибка API: {response.status_code}")
                break

            data = response.json()

            items = data.get('items', [])
            all_vacancies.extend(items)

            # Проверяем наличие следующей страницы
            pages = data.get('pages', 0)
            current_page = data.get('page', 0)
            if current_page >= pages - 1:
                break

            params['page'] += 1
            time.sleep(1)
        return all_vacancies


if __name__ == "__main__":
    api = HHVacanciesAPI()
    keyword = "python разработчик"
    vacancies = api.get_vacancies(keyword)
    vacancies_ = []
    for v in vacancies:
        if v.get('salary') is not None:
            vacancies_.append(v)

    print(f"Найдено {len(vacancies_)} вакансий с указанием зарплаты по запросу '{keyword}':")
    for v in vacancies_[:5]:  # показываем первые 5
        name = v.get('name')
        url = v.get('alternate_url')
        salary = v.get('salary')
        print(f"Вакансия: {name}")
        print(f"Ссылка: {url}")
        print(f"Зарплата: {salary}")
