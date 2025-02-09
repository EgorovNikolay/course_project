from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (
    filter_func,
    func_open_excel_file,
    func_open_json_file,
    get_currency_rates,
    get_stock_prices,
    get_top_transactions,
    greeting,
    result_bank_cards,
)


def test_func_open_json_file_success(mock_json_data):
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        result = func_open_json_file("dummy_path.json")
        assert result == {"user_currencies": ["USD", "EUR"]}


def test_func_open_json_file_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = func_open_json_file("nonexistent_path.json")
        assert result == {}


def test_func_open_json_file_json_decode_error():
    mock_data = "invalid_json"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = func_open_json_file("invalid_json_path.json")
        assert result == {}


@pytest.mark.parametrize(
    "time_str, expected_greeting",
    [
        ("2023-10-25 08:00:00", "Доброе утро"),
        ("2023-10-25 14:00:00", "Добрый день"),
        ("2023-10-25 20:00:00", "Добрый вечер"),
        ("2023-10-25 02:00:00", "Доброй ночи"),
        ("invalid_date", "Добрый день"),
    ],
)
def test_greeting(time_str, expected_greeting):
    result = greeting(time_str)
    assert result == expected_greeting


def test_func_open_excel_file_success(mock_excel_data):
    with patch("pandas.read_excel", return_value=mock_excel_data):
        result = func_open_excel_file("dummy_path.xlsx")
        assert not result.empty


def test_func_open_excel_file_file_not_found():
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = func_open_excel_file("nonexistent_path.xlsx")
        assert result.empty


def test_filter_func_success():
    data = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-10-01 12:00:00", "2023-10-15 14:30:00"]),
            "Сумма операции": [-1000, -2000],
            "Статус": ["OK", "OK"],
        }
    )
    result = filter_func(data, "2023-10-15 14:30:00")
    assert len(result) == 2


def test_result_bank_cards_success(mock_bank_cards_data):
    result = result_bank_cards(mock_bank_cards_data)
    assert len(result["cards"]) == 1
    assert result["cards"][0]["last_digits"] == "3456"


def test_result_bank_cards_empty_data():
    data = pd.DataFrame()
    result = result_bank_cards(data)
    assert result == {"cards": []}


def test_get_top_transactions_success(mock_transactions_data):
    result = get_top_transactions(mock_transactions_data)
    assert len(result["top_transactions"]) == 2


def test_get_top_transactions_empty_data():
    data = pd.DataFrame()
    result = get_top_transactions(data)
    assert result == {"top_transactions": []}


def test_get_currency_rates_success(mock_api_response):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_api_response
        result = get_currency_rates({"user_currencies": ["USD"]})
        assert result == {"currency_rates": [{"currency": "USD", "rate": 75.5}]}


def test_get_currency_rates_api_error():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        result = get_currency_rates({"user_currencies": ["USD"]})
        assert result == {"currency_rates": []}


def test_get_stock_prices_success():
    mock_response = {"Global Quote": {"05. price": "150.12"}}
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        result = get_stock_prices({"user_stocks": ["AAPL"]})
        assert result == {"stock_prices": [{"stock": "AAPL", "price": 150.12}]}


def test_get_stock_prices_api_error():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        result = get_stock_prices({"user_stocks": ["AAPL"]})
        assert result == {"stock_prices": []}
