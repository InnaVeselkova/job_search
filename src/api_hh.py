import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any

import requests


class VacanciesAPI(ABC):
    @abstractmethod
    def _connect(self) -> None:
        """Приватный метод проверки соединения с API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получить список вакансий по ключевому слову."""
        pass


class HHVacanciesAPI(VacanciesAPI):
    """Получение вакансий из API по поисковому запросу"""
    def __init__(self) -> None:
        self.__base_url: str = 'https://api.hh.ru/vacancies'
        self.__headers: Dict[str, str] = {'User-Agent': 'MyVacancyApp'}
        self._connect()

    def _connect(self):
        """
        Проверка соединения с API hh.ru.
        Выполняет GET-запрос к базовому URL и проверяет статус.
        В случае успеха выводит сообщение, иначе выбрасывает исключение.
        """
        response = requests.get(self.__base_url)
        if response.status_code == 200:
            print("Подключение успешно к hh.ru")
        else:
            raise ConnectionError(f"Ошибка подключения: {response.status_code}")

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получает список вакансий по ключевому слову
        """
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
