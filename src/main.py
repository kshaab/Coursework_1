import json

import pandas as pd

from src.reports import spending_by_category
from src.services import find_phone_transactions, get_transactions, investment_bank
from src.views import view_homepage


def main():
    """Объединяет работу модулей в единую программу"""

    try:
        excel_data = "../data/operations.xlsx"
        input_date = "2020-12-22 10:30:06"

        homepage_result = view_homepage(input_date)
        print("Главная страница:")
        print(json.dumps(homepage_result, indent=2, ensure_ascii=False))

        filtered_transactions = get_transactions("2021-12", excel_data)

        investment_result = investment_bank("2021-12", filtered_transactions, 10)
        print("Инвесткопилка:")
        print(json.dumps(investment_result, ensure_ascii=False, indent=2))

        phone_tx_result = find_phone_transactions(excel_data)
        print("Телефонные транзакции:")
        print(phone_tx_result)

        raw_transactions = pd.read_excel(excel_data)
        report = spending_by_category(raw_transactions, "Транспорт", "2019-11-16")
        print("Отчет по категории:")
        print(json.dumps(report, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
