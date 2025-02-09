from unittest.mock import patch

import pandas as pd

from src.views import generate_json_response


@patch("src.views.func_open_json_file")
@patch("src.views.func_open_excel_file")
@patch("src.views.filter_func")
@patch("src.views.result_bank_cards")
@patch("src.views.get_top_transactions")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
@patch("src.views.greeting")
def test_generate_json_response(
    mock_greeting,
    mock_get_stock_prices,
    mock_get_currency_rates,
    mock_get_top_transactions,
    mock_result_bank_cards,
    mock_filter_func,
    mock_func_open_excel_file,
    mock_func_open_json_file,
):
    mock_func_open_json_file.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mock_func_open_excel_file.return_value = pd.DataFrame(
        {
            "Дата операции": ["2020-03-15 14:30:00"],
            "Сумма операции": [-1000],
            "Статус": ["OK"],
            "Номер карты": ["1234567890123456"],
            "Категория": ["Food"],
            "Описание": ["Lunch"],
        }
    )
    mock_filter_func.return_value = pd.DataFrame(
        {
            "Дата операции": ["2020-03-15 14:30:00"],
            "Сумма операции": [-1000],
            "Статус": ["OK"],
            "Номер карты": ["1234567890123456"],
            "Категория": ["Food"],
            "Описание": ["Lunch"],
        }
    )
    mock_result_bank_cards.return_value = {"cards": [{"last_digits": "3456", "total_spent": 1000, "cashback": 10}]}
    mock_get_top_transactions.return_value = {
        "top_transactions": [{"date": "15.03.2020", "amount": -1000, "category": "Food", "description": "Lunch"}]
    }
    mock_get_currency_rates.return_value = {"currency_rates": [{"currency": "USD", "rate": 75.0}]}
    mock_get_stock_prices.return_value = {"stock_prices": [{"stock": "AAPL", "price": 150.0}]}
    mock_greeting.return_value = "Добрый день"
    result = generate_json_response("2020-03-15 14:30:00", "dummy_excel_path.xlsx", "dummy_json_path.json")
    expected_result = {
        "greeting": "Добрый день",
        "cards": [{"last_digits": "3456", "total_spent": 1000, "cashback": 10}],
        "top_transactions": [{"date": "15.03.2020", "amount": -1000, "category": "Food", "description": "Lunch"}],
        "currency_rates": [{"currency": "USD", "rate": 75.0}],
        "stock_prices": [{"stock": "AAPL", "price": 150.0}],
    }

    assert result == expected_result


@patch("src.views.func_open_json_file")
@patch("src.views.func_open_excel_file")
def test_generate_json_response_file_not_found(mock_func_open_excel_file, mock_func_open_json_file):
    mock_func_open_json_file.return_value = {}
    mock_func_open_excel_file.return_value = pd.DataFrame()
    result = generate_json_response("2020-03-15 14:30:00", "dummy_excel_path.xlsx", "dummy_json_path.json")
    assert result == {}
