import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

env_path = os.path.join("..", ".env")
load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")
API_KEY_2 = os.getenv("API_KEY_2")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def func_open_json_file(filepath: str) -> dict:
    """Функция читает json - файл"""
    try:
        with open(filepath, "r") as user_json_file:
            user_data = json.load(user_json_file)
            logging.info(f"JSON-файл успешно прочитан из {filepath}")
            return user_data
    except FileNotFoundError:
        logging.error(f"Файл {filepath} не найден")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Ошибка декодирования JSON-файла из {filepath}")
        return {}


def greeting(date: str) -> str:
    """Функция приветствует пользователя, в зависимости от времени"""
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        hour = date_obj.hour
        if 0 <= hour <= 5:
            greeting_message = "Доброй ночи"
        elif 6 <= hour <= 11:
            greeting_message = "Доброе утро"
        elif 12 <= hour <= 17:
            greeting_message = "Добрый день"
        else:
            greeting_message = "Добрый вечер"
        logging.info(f"Приветствие сгенерировано: {greeting_message}")
        return greeting_message
    except ValueError:
        logging.error(f"Неверный формат даты: {date}")
        return "Добрый день"


def func_open_excel_file(filepath: str) -> pd.DataFrame:
    """Функция читает excel - файл"""
    try:
        data_frame = pd.read_excel(filepath)
        data_frame["Дата операции"] = pd.to_datetime(
            data_frame["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
        )
        logging.info(f"Excel-файл успешно прочитан из {filepath}")
        return data_frame
    except FileNotFoundError:
        logging.error(f"Файл {filepath} не найден")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Ошибка при чтении Excel-файла: {e}")
        return pd.DataFrame()


def filter_func(data: pd.DataFrame, user_date: str) -> pd.DataFrame:
    """Фильтрует данные по диапазону дат: с начала месяца до входящей даты"""
    try:
        logging.info(f"Начало фильтрации данных по дате: {user_date}")
        user_date_obj = datetime.datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")
        start_filtered_date = user_date_obj.replace(day=1, hour=0, minute=0, second=0)
        end_filtered_date = user_date_obj
        if not pd.api.types.is_datetime64_any_dtype(data["Дата операции"]):
            logging.warning("Столбец 'Дата операции' не является datetime, выполняем преобразование")
            data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
        filtered_data = data[
            (data["Дата операции"] >= start_filtered_date) & (data["Дата операции"] <= end_filtered_date)
        ]
        logging.info(f"Данные отфильтрованы за период: {start_filtered_date} - {end_filtered_date}")
        return filtered_data
    except ValueError as e:
        logging.error(f"Ошибка при обработке даты: {e}")
        return pd.DataFrame()


def result_bank_cards(data: pd.DataFrame) -> dict:
    """Функция возвращает последние 4 цифры всех банковских карт, общую сумму и кэшбэк"""
    try:
        logging.info("Начало анализа данных по банковским картам")
        if data.empty:
            logging.warning("Данные пустые, результат по картам будет пустым")
            return {"cards": []}

        filtered_data = data[(data["Сумма операции"] < 0) & (data["Статус"] == "OK")]
        grouped_data = filtered_data.groupby("Номер карты")["Сумма операции"].sum().reset_index()
        grouped_data["cashback"] = grouped_data["Сумма операции"].abs() * 0.01
        cards = [
            {
                "last_digits": str(row["Номер карты"])[-4:] if isinstance(row["Номер карты"], str) else "N/A",
                "total_spent": round(abs(row["Сумма операции"]), 2),
                "cashback": round(row["cashback"], 2),
            }
            for _, row in grouped_data.iterrows()
        ]
        logging.info(f"Анализ данных по картам завершен, найдено {len(cards)} карт")
        return {"cards": cards}
    except Exception as e:
        logging.error(f"Ошибка при анализе данных по картам: {e}")
        return {"cards": []}


def get_top_transactions(data: pd.DataFrame) -> dict:
    """Функция возвращает топ-5 транзакций по сумме"""
    try:
        logging.info("Начало анализа топ-5 транзакций")
        if data.empty:
            logging.warning("Данные пустые, топ-транзакции будут пустыми")
            return {"top_transactions": []}
        filtered_data = data[(data["Сумма операции"] < 0) & (data["Статус"] == "OK")]
        top_five = filtered_data.sort_values(by="Сумма операции", key=abs, ascending=False).head(5)
        result = [
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(row["Сумма операции"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
            for _, row in top_five.iterrows()
        ]
        logging.info(f"Анализ топ-5 транзакций завершен, найдено {len(result)} транзакций")
        return {"top_transactions": result}
    except Exception as e:
        logging.error(f"Ошибка при анализе топ-транзакций: {e}")
        return {"top_transactions": []}


def get_currency_rates(user_currencies: dict) -> dict:
    """Функция получает курс валют в рублях"""
    try:
        logging.info("Начало получения курсов валют")
        rates = []
        currencies = user_currencies.get("user_currencies", [])
        for currency in currencies:
            url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"
            headers = {"apikey": API_KEY}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                rate = data["rates"]["RUB"]
                rates.append({"currency": currency, "rate": round(rate, 2)})
                logging.info(f"Курс валюты {currency} успешно получен: {rate}")
            else:
                logging.error(f"Ошибка при запросе курса для валюты {currency}: {response.status_code}")
        return {"currency_rates": rates}
    except Exception as e:
        logging.error(f"Ошибка при получении курсов валют: {e}")
        return {"currency_rates": []}


def get_stock_prices(user_stocks: dict) -> dict:
    """Функция получает стоимость акций"""
    try:
        logging.info("Начало получения стоимости акций")
        stock_prices = []
        stocks = user_stocks.get("user_stocks", [])
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY_2}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "Global Quote" in data:
                    price = float(data["Global Quote"]["05. price"])
                    stock_prices.append({"stock": stock, "price": round(price, 2)})
                    logging.info(f"Цена акции {stock} успешно получена: {price}")
            else:
                logging.error(f"Ошибка при запросе цены акции {stock}: {response.status_code}")
        return {"stock_prices": stock_prices}
    except Exception as e:
        logging.error(f"Ошибка при получении цен акций: {e}")
        return {"stock_prices": []}
