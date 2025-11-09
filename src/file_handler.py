import json
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Dict, Any

from src.vacancy import Vacancy


class FileHandler(ABC):
    @abstractmethod
    def add_data(self, data) -> None:
        """
        Добавление вакансий
        """
        pass

    @abstractmethod
    def get_data(self, filter_func: Optional[Callable[['dict'], bool]] = None) -> List[Dict[str, Any]]:
        """
        Позволяет получить все вакансии или фильтрованные по условию
        """
        pass

    @abstractmethod
    def delete_data(self, criteria: Callable[['dict'], bool]) -> None:
        """
        Удаление вакансии по заданному критерию
        """
        pass


class JSONFileHandler(FileHandler):
    """
    класс для сохранения информации о вакансиях в JSON-файл
    """
    def __init__(self, filename: str = 'vacancies.json') -> None:
        self.__filename: str = filename
        self._load()

    def _load(self) -> None:
        """
             Загружает данные из файла. В случае отсутствия файла
             инициализирует пустой список.
        """
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
                self._remove_duplicates()
        except FileNotFoundError:
            self._data = []

    def _save(self)-> None:
        """Сохраняет текущие данные в файл"""
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4)

    def _remove_duplicates(self) -> None:
        """
        Удаляет дублирующиеся вакансии из данных
        """
        seen = set()
        unique_data = []
        for item in self._data:
            item_str = json.dumps(item, sort_keys=True)
            if item_str not in seen:
                seen.add(item_str)
                unique_data.append(item)
        self._data = unique_data

    def add_data(self, vacancy: 'Vacancy') -> None:
        """
        Добавляет вакансию в хранилище, избегая дубликатов
        """
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

    def get_data(self, filter_func: Optional[Callable[[Dict[str, Any]], bool]] = None) -> List[Dict[str, Any]]:
        """
        Получает все вакансии или фильтрованные по функции
        """
        if filter_func is None:
            return self._data
        return list(filter(filter_func, self._data))

    def delete_data(self, criteria: Callable[[Dict[str, Any]], bool]) -> None:
        """
        удаляет вакансии в соответствии с критериями
        """
        self._data = list(filter(lambda v: not criteria(v), self._data))
        self._save()
