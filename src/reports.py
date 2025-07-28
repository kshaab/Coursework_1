import functools
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def save_report_to_file(file: Optional[str] = None) -> Callable:
    """Декоратор для записи отчета в файл"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            out_file = file
            if not out_file:
                date_str = datetime.now().strftime("%Y-%m-%d")
                out_file = f"report_{func.__name__}_{date_str}.json"

            try:
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                logger.info(f"Отчет сохранен в файл: {out_file}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")

            return result

        return wrapper

    return decorator


@save_report_to_file("spending_report.json")
def spending_by_category(t: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    """Возвращает траты по заданной категории за последние три месяца от переданной даты"""
    if date:
        try:
            current_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error("Неверный формат даты. Ожидается YYYY-MM-DD.")
            return {}
    else:
        current_date = datetime.today()

    three_months = current_date - timedelta(days=90)

    t["Дата платежа"] = pd.to_datetime(t["Дата платежа"], errors="coerce", dayfirst=True)
    df = t.dropna(subset=["Дата платежа", "Категория"])

    filtered = df[
        (df["Категория"].str.lower() == category.lower())
        & (df["Дата платежа"] >= three_months)
        & (df["Дата платежа"] <= current_date)
    ]

    total = abs(filtered["Сумма операции"].sum())
    return {
        "категория": category,
        "с": three_months.strftime("%Y-%m-%d"),
        "по": current_date.strftime("%Y-%m-%d"),
        "трат всего": round(total, 2),
        "транзакций": len(filtered),
    }


if __name__ == "__main__":
    excel_data = "../data/operations.xlsx"
    transactions = pd.read_excel(excel_data)
    report = spending_by_category(transactions, "Транспорт", "2019-11-16")
    print(json.dumps(report, indent=2, ensure_ascii=False))
