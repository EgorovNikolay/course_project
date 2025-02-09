import os
import json
import logging
import pandas as pd
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
from src.services import simple_search
from src.reports import spending_by_category


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


env_path = os.path.join("..", ".env")
load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")
API_KEY_2 = os.getenv("API_KEY_2")


def main():
    """Главная функция, объединяющая весь функционал проекта"""
    try:
        excel_filepath = os.path.join("..", "data", "operations.xlsx")
        json_filepath = os.path.join("..", "data", "user_settings.json")
        input_date = "2020-03-15 14:30:00"
        logging.info("Загрузка данных...")
        user_settings = func_open_json_file(json_filepath)
        transactions_data = func_open_excel_file(excel_filepath)
        filtered_data = filter_func(transactions_data, input_date)
        response = {
            "greeting": greeting(input_date),
            "cards": result_bank_cards(filtered_data).get("cards", []),
            "top_transactions": get_top_transactions(filtered_data).get("top_transactions", []),
            "currency_rates": get_currency_rates(user_settings).get("currency_rates", []),
            "stock_prices": get_stock_prices(user_settings).get("stock_prices", []),
        }
        logging.info("JSON-ответ успешно сформирован")
        print(json.dumps(response, ensure_ascii=False, indent=4))
        search_query = "Магнит"
        search_result = simple_search(search_query, response["top_transactions"])
        logging.info(f"Результаты поиска по запросу '{search_query}': {search_result}")

        df = pd.DataFrame(transactions_data)
        category_report = spending_by_category(df, "Фастфуд", date="2021-10-20")
        logging.info("Отчет по тратам в категории 'Фастфуд' сформирован")
        print(category_report)
    except Exception as e:
        logging.error(f"Ошибка в основном модуле: {e}")


if __name__ == "__main__":
    main()
