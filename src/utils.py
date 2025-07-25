import json
import logging as log
import os
from typing import Any, Dict, List, Union

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[log.FileHandler("app.log"), log.StreamHandler()],
)


def read_excel(excel_file: str) -> pd.DataFrame:
    """Читает данные из файла с операциями"""
    try:
        return pd.read_excel(excel_file)
    except Exception as e:
        log.error(f"Ошибка при чтении Excel-файла: {e}")
        return pd.DataFrame()


def read_json(json_file: str) -> Dict[str, Any]:
    """Читает файл с настройками пользователя"""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log.error(f"Ошибка при чтении JSON-файла: {e}")
        return {}


def filter_by_date(df: pd.DataFrame, date: Union[str, pd.Timestamp]) -> pd.DataFrame:
    """Фильтрует диапазон от начала месяца до заданной даты включительно"""
    target_date = pd.to_datetime(date)
    month_start = target_date.replace(day=1)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    return df[(df["Дата платежа"] >= month_start) & (df["Дата платежа"] <= target_date)]


def view_cards_info(df: pd.DataFrame, date: Union[str, pd.Timestamp]) -> list[dict[str, Any]]:
    """Выводит данные по картам"""
    df = filter_by_date(df, date).copy()
    df["last_digits"] = df["Номер карты"].astype(str).str[-4:]
    df["last_digits"] = df["last_digits"].replace("nan", "Неизвестный номер карты")
    df["total_spent"] = round(df["Сумма операции"].abs())
    total = df.groupby("last_digits")["total_spent"].sum().reset_index()
    total["cashback"] = (total["total_spent"] // 100).astype(int)
    return total.to_dict(orient="records")


def search_top(df: pd.DataFrame, date: Union[str, pd.Timestamp]) -> list[dict[str, Any]]:
    """Собирает топ-5 операций по сумме платежа"""
    df = filter_by_date(df, date).copy()
    df["date"] = df["Дата платежа"].astype(str)
    df["amount"] = df["Сумма операции"].abs()
    df["category"] = df["Категория"].astype(str)
    df["description"] = df["Описание"].astype(str)
    top = df.sort_values(by="amount", ascending=False).head(5)
    top = top[["date", "amount", "category", "description"]]
    return top.to_dict(orient="records")


def view_exchange_rate(settings: Dict[str, Any]) -> List[Dict[str, Union[str, float, None]]]:
    """Выводит текущий курс валют, в зависимости от настроенных валют пользователя"""
    result_list = []
    api_key = os.getenv("API_KEY_EXCHANGE")
    user_currencies = settings.get("user_currencies", [])

    symbols = ",".join(set(user_currencies + ["RUB"]))
    url = f"http://data.fixer.io/api/latest?access_key={api_key}&symbols={symbols}"

    response = requests.get(url)
    data = response.json()

    if not data.get("success"):
        raise Exception(f"API Error: {data.get('error')}")

    rates = data["rates"]
    rub_rate = rates.get("RUB")

    for currency in user_currencies:
        if currency not in rates:
            result_list.append({"currency": currency, "rate": None})
            continue
        if currency == "RUB":
            rate = 1.00
        else:
            rate = round(rub_rate / rates[currency], 2)
        result_list.append({"currency": currency, "rate": rate})

    return result_list


def view_stock_prices(settings: Dict[str, Any]) -> List[Dict[str, Union[str, float, None]]]:
    """Выводит стоимость акций в зависимости от настроенных акций пользователя"""
    results = []
    api_key = os.getenv("API_KEY_PROMOTION")
    user_stocks = settings.get("user_stocks", [])

    for stock in user_stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        quote = data.get("Global Quote", {})
        price_str = quote.get("05. price")

        if price_str:
            price = round(float(price_str), 2)
            results.append({"stock": stock, "price": price})
        else:
            results.append({"stock": stock, "price": None})

    # print(json.dumps(results, indent=2))
    # закомиченно для избежания дублирования в основной функции
    return results


if __name__ == "__main__":
    # проверка работы функций в этом модуле
    excel_data = "../data/operations.xlsx"
    read_data = read_excel(excel_data)
    required_date = "2020-11-06"
    result = view_cards_info(read_data, required_date)
    top_operations = search_top(read_data, required_date)
    json_data = "../user_settings.json"
    read = read_json(json_data)
    for card in result:
        print(card)
    for row in top_operations:
        print(json.dumps(row, indent=2, ensure_ascii=False))

    print(view_exchange_rate(read))
    view_stock_prices(read)
