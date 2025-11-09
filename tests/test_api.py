from unittest.mock import Mock, patch

import pytest

from src.api_hh import HHVacanciesAPI


@patch('requests.get')
def test_get_vacancies_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'items': [{'id': '1'}],
        'pages': 1,
        'page': 0
    }
    mock_get.return_value = mock_response

    api = HHVacanciesAPI()
    result = api.get_vacancies('Python')

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['id'] == '1'
    assert mock_get.called


@patch('requests.get')
def test_get_vacancies_api_error_in_connect(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    # При создании объекта вызовется _connect(), которая выбросит исключение
    with pytest.raises(ConnectionError):
        HHVacanciesAPI()
