from src.api_hh import HHVacancyAPI
from src.file_handler import JSONFileHandler
from src.user_interaction import user_interaction

if __name__ == "__main__":
    api = HHVacancyAPI()
    storage = JSONFileHandler()
    user_interaction(api, storage)