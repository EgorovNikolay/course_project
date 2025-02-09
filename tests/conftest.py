import pandas as pd
import pytest


@pytest.fixture
def mock_json_data():
    return '{"user_currencies": ["USD", "EUR"]}'


@pytest.fixture
def mock_excel_data():
    return pd.DataFrame(
        {
            "Дата операции": ["01.10.2023 12:00:00", "02.10.2023 14:30:00"],
            "Сумма операции": [-1000, -2000],
            "Статус": ["OK", "OK"],
        }
    )


@pytest.fixture
def mock_bank_cards_data():
    return pd.DataFrame(
        {
            "Номер карты": ["1234567890123456", "1234567890123456"],
            "Сумма операции": [-1000, -2000],
            "Статус": ["OK", "OK"],
        }
    )


@pytest.fixture
def mock_transactions_data():
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-10-01 12:00:00", "2023-10-15 14:30:00"]),
            "Сумма операции": [-1000, -2000],
            "Статус": ["OK", "OK"],
            "Категория": ["Супермаркеты", "Транспорт"],
            "Описание": ["Покупка", "Такси"],
        }
    )


@pytest.fixture
def mock_api_response():
    return {"rates": {"RUB": 75.5}}


@pytest.fixture
def transactions_data():
    return [
        {"id": 1, "description": "Покупка продуктов", "category": "Еда", "amount": 1000},
        {"id": 2, "description": "Оплата интернета", "category": "Коммунальные услуги", "amount": 500},
        {"id": 3, "description": "Покупка книги", "category": "Образование", "amount": 300},
        {"id": 4, "description": "Кофе", "category": "Еда", "amount": 150},
    ]


@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": ["2023-09-01", "2023-08-15", "2023-07-10", "2023-06-05", "2023-05-01"],
        "Категория": ["Еда", "Транспорт", "Еда", "Еда", "Одежда"],
        "Сумма": [100, 200, 150, 300, 400],
    }
    return pd.DataFrame(data)
