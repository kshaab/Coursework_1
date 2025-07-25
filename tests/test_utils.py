import pytest
from unittest.mock import patch, mock_open
import pandas as pd


from src.utils import (
    read_excel,
    read_json,
    filter_by_date,
    view_cards_info,
    search_top,
    view_exchange_rate,
    view_stock_prices,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Дата платежа": pd.to_datetime(["2020-11-01", "2020-11-03", "2020-11-10"]),
            "Сумма операции": [-100.0, -250.0, -50.0],
            "Номер карты": ["*1234", "*5678", "*1234"],
            "Категория": ["Супермаркеты", "Каршеринг", "Фастфуд"],
            "Описание": ["Магнит", "Ситидрайв", "Mouse Tail"],
        }
    )


@pytest.mark.parametrize("date,expected_len", [("2020-11-06", 2), ("2020-11-30", 3), ("2020-11-01", 1)])
def test_filter_by_date(sample_df, date, expected_len):
    filtered = filter_by_date(sample_df.copy(), date)
    assert len(filtered) == expected_len


def test_view_cards_info(sample_df):
    result = view_cards_info(sample_df.copy(), pd.to_datetime("2020-11-30"))
    assert isinstance(result, list)
    assert all("last_digits" in card and "total_spent" in card and "cashback" in card for card in result)


def test_search_top(sample_df):
    result = search_top(sample_df.copy(), pd.to_datetime("2020-11-30"))
    assert isinstance(result, list)
    assert len(result) <= 5
    assert all("date" in tx and "amount" in tx for tx in result)


def test_read_excel_success(tmp_path):
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1]})
    df.to_excel(test_file, index=False)
    result = read_excel(str(test_file))
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_read_json_success(mock_file):
    result = read_json("dummy.json")
    assert result["key"] == "value"


@patch("requests.get")
def test_view_exchange_rate_success(mock_get):
    mock_get.return_value.json.return_value = {"success": True, "rates": {"USD": 1.2, "RUB": 90.0}}
    settings = {"user_currencies": ["USD"]}
    rates = view_exchange_rate(settings)
    assert rates[0]["currency"] == "USD"
    assert isinstance(rates[0]["rate"], float)


@patch("requests.get")
def test_view_stock_prices_success(mock_get):
    mock_get.return_value.json.return_value = {"Global Quote": {"05. price": "123.45"}}
    settings = {"user_stocks": ["AAPL"]}
    stocks = view_stock_prices(settings)
    assert stocks[0]["stock"] == "AAPL"
    assert stocks[0]["price"] == 123.45
