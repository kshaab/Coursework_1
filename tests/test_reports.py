from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def df_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата платежа": pd.to_datetime(
                [
                    "2019-08-20",  # попадает в диапазон
                    "2019-09-15",  # попадает
                    "2019-06-01",  # не попадает
                ]
            ),
            "Сумма операции": [-100.0, -250.0, -300.0],
            "Категория": ["Транспорт", "Транспорт", "Транспорт"],
        }
    )


def test_spending_by_category_correct(df_transactions: pd.DataFrame) -> None:
    report = spending_by_category(df_transactions, "транспорт", "2019-11-16")
    assert report["категория"] == "транспорт"
    assert report["трат всего"] == 350.0
    assert report["транзакций"] == 2
    assert report["с"] == "2019-08-18"
    assert report["по"] == "2019-11-16"


def test_spending_by_category_wrong_date(df_transactions: pd.DataFrame, caplog: pytest.LogCaptureFixture) -> None:
    report = spending_by_category(df_transactions, "транспорт", "16-11-2019")
    assert report == {}
    assert "Неверный формат даты" in caplog.text


@patch("builtins.open", new_callable=mock_open)
def test_spending_by_category_saves_to_file(mock_file: MagicMock, df_transactions: pd.DataFrame) -> None:
    with patch("src.reports.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2020, 1, 1)
        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(*args, **kwargs)

        spending_by_category(df_transactions, "транспорт", "2019-11-16")
        mock_file.assert_called_once_with("spending_report.json", "w", encoding="utf-8")
        handle = mock_file()
        saved_content = "".join(call.args[0] for call in handle.write.call_args_list)
        assert '"трат всего": 350.0' in saved_content
