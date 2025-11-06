from src.api_hh import VacancyAPI
from src.file_handler import VacancyFileHandler
from src.vacancy import Vacancy


def user_interaction(api: VacancyAPI, storage: VacancyFileHandler):
    print("Добро пожаловать!")

    search_query = input("Введите поисковый запрос: ")
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    except ValueError:
        print("Некорректный ввод для N, устанавливаем N=5.")
        top_n = 5

    filter_words_input = input("Введите ключевые слова для фильтрации (через пробел): ")
    filter_words = filter_words_input.lower().split()

    salary_range_input = input("Введите диапазон зарплат (например, 100000-150000 или оставить пустым): ")
    salary_min, salary_max = None, None
    if salary_range_input.strip():
        try:
            parts = salary_range_input.replace(' ', '').split('-')
            if len(parts) == 2:
                salary_min = int(parts[0])
                salary_max = int(parts[1])
        except ValueError:
            print("Некорректный формат диапазона. Игнорируем фильтр по зарплате.")

    # Получение вакансий из API по поисковому запросу
    vacancies_data = api.get_vacancies(search_query)

    # Фильтрация по ключевым словам в описании
    if filter_words:
        def filter_func(v):
            description = v.get('description') or ''
            return all(word in description.lower() for word in filter_words)
        filtered = list(filter(filter_func, vacancies_data))
    else:
        filtered = vacancies_data

    # Создаем объекты Vacancy для сортировки по зарплате
    vacancies_objs = []
    for v in filtered:
        salary = v.get('salary')
        vacancy_obj = Vacancy(
            name=v.get('name', 'Без названия'),
            url=v.get('alternate_url', ''),
            salary=salary,
            description=v.get('description', ''),
            requirements=v.get('requirements', '')
        )
        vacancies_objs.append(vacancy_obj)

    # Фильтр по диапазону зарплат
    if salary_min is not None and salary_max is not None:
        def salary_filter(v: Vacancy):
            val = v._get_salary_value()
            return salary_min <= val <= salary_max
        vacancies_objs = list(filter(salary_filter, vacancies_objs))

    # Сортировка по зарплате
    sorted_vacancies = sorted(vacancies_objs, reverse=True)

    # Вывод топ N вакансий
    for v in sorted_vacancies[:top_n]:
        print(f"Вакансия: {v.name}")
        print(f"Зарплата: {v.salary}")
        print(f"Ссылка: {v.url}")
