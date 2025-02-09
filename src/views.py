import json
import logging
import os

from dotenv import load_dotenv

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

env_path = os.path.join("..", ".env")
load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")
API_KEY_2 = os.getenv("API_KEY_2")


def generate_json_response(date: str, excel_filepath: str, json_filepath: str) -> dict:
    """Функция генерирует JSON-ответ на основе входных данных"""
    try:
        logging.info(f"Генерация JSON-ответа для даты: {date}")
        user_settings = func_open_json_file(json_filepath)
        transactions_data = func_open_excel_file(excel_filepath)
        filtered_data = filter_func(transactions_data, date)
        greeting_message = greeting(date)
        cards_info = result_bank_cards(filtered_data).get("cards", [])
        if not cards_info:
            logging.warning("Данные по картам отсутствуют")
        top_transactions = get_top_transactions(filtered_data).get("top_transactions", [])
        if not top_transactions:
            logging.warning("Топ-транзакции отсутствуют")
        currency_rates = get_currency_rates(user_settings).get("currency_rates", [])
        if not currency_rates:
            logging.warning("Данные о курсах валют отсутствуют")
        stock_prices = get_stock_prices(user_settings).get("stock_prices", [])
        if not stock_prices:
            logging.warning("Данные о ценах акций отсутствуют")
        response = {
            "greeting": greeting_message,
            "cards": cards_info,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }
        logging.info("JSON-ответ успешно сформирован")
        return response
    except Exception as e:
        logging.error(f"Ошибка при генерации JSON-ответа: {e}")
        return {}


excel_filepath = os.path.join("..", "data", "operations.xlsx")
json_filepath = os.path.join("..", "data", "user_settings.json")
input_date = "2020-03-15 14:30:00"


result = generate_json_response(input_date, excel_filepath, json_filepath)
print(json.dumps(result, ensure_ascii=False, indent=4))
