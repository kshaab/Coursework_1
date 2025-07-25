import pytest
from unittest.mock import patch
import pandas as pd
from src.views import view_homepage


@pytest.fixture
def mock_df():
    return pd.DataFrame(
        {
            "Дата платежа": pd.to_datetime(["2020-11-01", "2020-11-03", "2020-11-10"]),
            "Сумма операции": [-100.0, -250.0, -50.0],
            "Номер карты": ["*1234", "*5678", "*1234"],
            "Категория": ["Супермаркеты", "Каршеринг", "Фастфуд"],
            "Описание": ["Магнит", "Ситидрайв", "Mouse Tail"],
        }
    )


@pytest.fixture
def mock_user_settings():
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOG"]}


@patch("src.utils.read_excel")
@patch("src.utils.read_json")
@patch("src.utils.view_cards_info")
@patch("src.utils.search_top")
@patch("src.utils.view_exchange_rate")
@patch("src.utils.view_stock_prices")
def test_view_homepage(
    mock_stock_prices,
    mock_exchange_rate,
    mock_search_top,
    mock_view_cards_info,
    mock_read_json,
    mock_read_excel,
    mock_df,
    mock_user_settings,
):

    mock_read_excel.return_value = mock_df
    mock_read_json.return_value = mock_user_settings

    mock_view_cards_info.return_value = [{"last_digits": "3456", "total_spent": 500, "cashback": 5}]
    mock_search_top.return_value = [
        {"date": "2020-12-15", "amount": 1500, "category": "Транспорт", "description": "Такси"}
    ]
    mock_exchange_rate.return_value = [{"currency": "USD", "rate": 91.0}]
    mock_stock_prices.return_value = [{"stock": "AAPL", "price": 171.0}]

    result = view_homepage("2020-12-22 10:30:06")

    assert "greeting" in result
    assert result["greeting"] in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]

    assert result["cards"][0]["last_digits"] == "4556"
    assert isinstance(result["top_transactions"], list)
    assert isinstance(result["currency_rates"], list)
    assert isinstance(result["stock_prices"], list)
