from typing import List, Optional
from src.api_hh import HHVacanciesAPI
from src.parsers import parse_vacancies
from src.vacancy import Vacancy


def user_interaction()-> List['Vacancy']:
    """
    функция для взаимодействия с пользователем
    """
    print("Добро пожаловать!")

    search_query = input("Введите поисковый запрос: ")
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    except ValueError:
        print("Некорректный ввод для N, устанавливаем N=5.")
        top_n = 5

    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    salary_range = input("Введите диапазон зарплат (например, 100000-150000 или оставить пустым): ")
    salary_min, salary_max = None, None
    if salary_range.strip():
        try:
            parts = salary_range.replace(' ', '').split('-')
            if len(parts) == 2:
                salary_min = int(parts[0])
                salary_max = int(parts[1])
        except ValueError:
            print("Некорректный формат диапазона. Игнорируем фильтр по зарплате.")

    # Получение вакансий из API по поисковому запросу
    api = HHVacanciesAPI()
    vacancies_data = api.get_vacancies(search_query)

    # Фильтрация по ключевым словам в описании
    if filter_words:
        def filter_func(v):
            description = v.get('description') or ''
            return all(word in description.lower() for word in filter_words)
        filtered = list(filter(filter_func, vacancies_data))
    else:
        filtered = vacancies_data

    vacancies = parse_vacancies(filtered)

    if salary_min is not None and salary_max is not None:
        v: Vacancy
        vacancies = list(filter(lambda v: salary_min <= v._get_salary_value() <= salary_max, vacancies))

    # Сортировка по зарплате (по убыванию)
    top_vacancies = sorted(vacancies, key=lambda v: v._get_salary_value(), reverse=True)[:top_n]
    return top_vacancies
