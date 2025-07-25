import datetime
import json
from typing import Any, Dict

import pandas as pd

from src.utils import read_excel, read_json, search_top, view_cards_info, view_exchange_rate, view_stock_prices

excel_data = "../data/operations.xlsx"
json_data = "../user_settings.json"


def greeting() -> str:
    """Отображает приветствие в зависимости от времени суток"""
    current_time = datetime.datetime.now().time()
    morning = datetime.time(5, 0, 0)
    day = datetime.time(12, 0, 0)
    evening = datetime.time(18, 0, 0)
    night = datetime.time(23, 0, 0)

    if morning <= current_time < day:
        return "Доброе утро"
    elif day <= current_time < evening:
        return "Добрый день"
    elif evening <= current_time < night:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def view_homepage(date: str) -> Dict[str, Any]:
    """Объединяет работу вспомогательных функций и возвращает JSON-ответ"""
    target_date = pd.to_datetime(date)

    df = read_excel(excel_data)
    user_settings = read_json(json_data)

    cards_info = view_cards_info(df, target_date)
    top_operations = search_top(df, target_date)
    exchange = view_exchange_rate(user_settings)
    stocks = view_stock_prices(user_settings)

    return {
        "greeting": greeting(),
        "cards": cards_info,
        "top_transactions": top_operations,
        "currency_rates": exchange,
        "stock_prices": stocks,
    }


if __name__ == "__main__":
    input_date = "2020-12-22 10:30:06"
    report = view_homepage(input_date)
    print(json.dumps(report, indent=2, ensure_ascii=False))
