from abc import ABC, abstractmethod
import requests
import time


class VacancyAPI(ABC):
    @abstractmethod
    def connect(self):
        """Подключение к API."""
        pass

    @abstractmethod
    def get_vacancies(self, query: str, params: dict = None):
        """Получение списка вакансий из API."""
        pass


class HHVacancyAPI(VacancyAPI):
    def __init__(self):
        self.base_url = 'https://api.hh.ru/vacancies'

    def connect(self):
        # Для hh.ru API не требуется авторизация, есть ограничения по скорости
        pass

    def get_vacancies(self, query: str, params: dict = None):
        params = params or {}
        params['text'] = query
        vacancies = []
        page = 0
        while True:
            params['page'] = page
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                break
            data = response.json()
            vacancies.extend(data['items'])
            if data['pages'] == page:
                break
            page += 1
            time.sleep(0.3)  # чтобы не превышать лимит
        return vacancies