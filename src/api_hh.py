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
        self.__base_url = 'https://api.hh.ru/vacancies'
        self.__connect()

    def __connect(self):
        """Приватный метод подключения к API - проверка базового URL."""
        response = requests.get(self.__base_url)
        if response.status_code == 200:
            print("Подключение успешно.")
        else:
            raise ConnectionError(f"Не удалось подключиться к API: статус {response.status_code}")


    def connect(self):
        """Реализуем абстрактный метод."""
        self.__connect()

    def get_vacancies(self, keyword: str, per_page: int = 20):
        """Получает вакансии по ключевому слову и возвращает список словарей из ключа 'items'."""

        params = {
            'text': keyword,
            'per_page': per_page
        }

        vacancies = []
        page = 0
        while True:
            try:
                #self.__connect()

                params['page'] = page
                response = requests.get(self.__base_url, params=params)

                if response.status_code != 200:
                    print(f"Ошибка API: {response.status_code}")
                    break

                data = response.json()

                # Собираем вакансии из ключа 'items'
                page_items = data.get('items', [])
                vacancies.extend(page_items)

                # Проверяем наличие следующей страницы
                total_pages = data.get('pages', 0)
                if page >= total_pages - 1:
                    break
                page += 1
                time.sleep(1)
            except requests.RequestException as e:
                print(f"Ошибка соединения: {e}")
                print("Повтор через несколько секунд...")
                time.sleep(5)
                continue
        return vacancies


if __name__ == "__main__":

    api = HHVacancyAPI()
    vacancies = api.get_vacancies("Python разработчик")
    print(vacancies)
