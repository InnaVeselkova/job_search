from src.file_handler import JSONFileHandler
from src.user_interaction import user_interaction


if __name__ == "__main__":
    vacancies = user_interaction()
    handler = JSONFileHandler()
    for v in vacancies:
        handler.add_data(v)
