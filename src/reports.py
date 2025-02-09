import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


def report_to_file(filename="default_report.json"):
    """Декоратор для записи результата функции в файл"""

    def wrapper(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                if isinstance(result, pd.DataFrame):
                    result_json = result.to_json(orient="records", force_ascii=False, indent=4)
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(result_json)
                    logging.info(f"Данные успешно записаны в файл: {filename}")
                else:
                    logging.error("Результат функции не является DataFrame и не может быть записан в файл.")
            except Exception as e:
                logging.error(f"Ошибка при записи в файл: {e}")
            return result

        return inner

    return wrapper


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца"""
    try:
        if transactions.empty:
            logging.error("Переданный DataFrame пуст!")
            return pd.DataFrame({"error": ["Переданный DataFrame пуст"]})
        logging.info(f"Начало формирования отчета по категории: {category}")

        logging.info(f"Столбцы в transactions: {transactions.columns.tolist()}")
        logging.info(f"Типы данных в transactions:\n{transactions.dtypes}")
        logging.info(f"Первые строки transactions:\n{transactions.head()}")
        if "Дата операции" not in transactions.columns:
            logging.error("Отсутствует столбец 'Дата операции' в DataFrame")
            return pd.DataFrame({"error": ["Отсутствует столбец 'Дата операции'"]})
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"], format="%Y-%m-%d", errors="coerce"
        )
        if transactions["Дата операции"].isna().any():
            logging.warning("Некоторые даты не удалось преобразовать в datetime!")
        end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        start_date = end_date - timedelta(days=90)
        logging.info(f"Период фильтрации: с {start_date} по {end_date}")
        filtered_transactions = transactions[
            (transactions["Категория"].str.lower() == category.lower())
            & (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
        ]
        logging.info(f"Отфильтрованные транзакции:\n{filtered_transactions}")
        if filtered_transactions.empty:
            logging.warning(f"Нет данных для категории: {category}")
        return filtered_transactions
    except Exception as e:
        logging.error(f"Ошибка при формировании отчета: {e}")
        return pd.DataFrame({"error": [str(e)]})
