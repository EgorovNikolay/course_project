import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def simple_search(search_query, transactions):
    """Функция для поиска транзакций по строке запроса"""
    try:
        logging.info(f"Начало поиска по запросу: {search_query}")
        filtered_transactions = [
            transaction
            for transaction in transactions
            if search_query.lower() in transaction.get("description", "").lower()
            or search_query.lower() in transaction.get("category", "").lower()
        ]
        result = json.dumps(filtered_transactions, ensure_ascii=False)
        logging.info(f"Поиск завершен. Найдено {len(filtered_transactions)} транзакций.")
        return result
    except Exception as e:
        logging.error(f"Ошибка при выполнении поиска: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)
