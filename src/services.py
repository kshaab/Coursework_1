import json
import logging as log
import math
import re
from typing import Any, Dict, List

import pandas as pd

from src.utils import read_excel

logger = log.getLogger(__name__)
log.basicConfig(level=log.INFO)


def get_transactions(month: str, excel_file: str) -> List[Dict[str, Any]]:
    """Собирает транзакции из файла в список словарей"""
    df = read_excel(excel_file)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    df_filtered = df[df["Дата платежа"].dt.strftime("%Y-%m") == month].copy()
    df_filtered["date"] = df_filtered["Дата платежа"].dt.strftime("%Y-%m-%d")
    df_filtered["amount"] = df_filtered["Сумма операции"].abs()
    return df_filtered[["date", "amount"]].to_dict(orient="records")


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Возвращает сумму, отложенную в Инвесткопилку"""
    logger.info(f"Начало расчета за месяц: {month}, лимит округления: {limit}")

    def calc_saving(t: Dict[str, Any]) -> float:
        """Рассчитывает сумму"""
        date = t["date"]
        amount = t["amount"]
        if date.startswith(month):
            rounded = math.ceil(amount / limit) * limit
            saved = rounded - amount
            logger.debug(f"Транзакция: {date}, сумма={amount}, округлено до {rounded}, отложено={saved}")
            return float(saved)
        return 0.0

    savings = list(map(calc_saving, transactions))
    total = round(sum(savings), 2)
    logger.info(f"Итоговая отложенная сумма за {month}: {total}")
    return total


def find_phone_transactions(excel_file: str) -> str:
    """Находит операции в файле, содержащие номер телефона в описании"""
    df = read_excel(excel_file)

    if df.empty:
        logger.warning("Файл пуст или не найден.")
        return json.dumps({"transactions": []}, ensure_ascii=False, indent=2)

    if "Описание" not in df.columns:
        logger.error("Колонка 'Описание' отсутствует в данных.")
        return json.dumps({"transactions": []}, ensure_ascii=False, indent=2)

    phone_pattern = re.compile(r"\+7\s?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}")

    filtered_rows = filter(lambda row: phone_pattern.search(str(row["Описание"])), df.to_dict(orient="records"))

    mapped_transactions = map(
        lambda row: {
            "date": str(row.get("Дата платежа", "")),
            "amount": abs(row.get("Сумма операции", 0)),
            "description": row["Описание"],
        },
        filtered_rows,
    )

    result = list(mapped_transactions)
    logger.info(f"Найдено {len(result)} транзакций с номерами телефонов.")
    return json.dumps({"transactions": result}, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    excel_data = "../data/operations.xlsx"
    transactions = get_transactions("2021-11", excel_data)
    result = investment_bank("2021-11", transactions, 10)
    result_json = find_phone_transactions(excel_data)
    print(result_json)
    print(json.dumps(result, ensure_ascii=False, indent=2))
