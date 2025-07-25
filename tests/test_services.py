import pytest
import json
from unittest.mock import patch
import pandas as pd
from src.services import get_transactions, investment_bank, find_phone_transactions


@pytest.fixture
def fake_transactions():
    return [
        {"date": "2021-12-01", "amount": 237.0},
        {"date": "2021-12-05", "amount": 415.5},
        {"date": "2021-12-20", "amount": 90.0},
    ]


@pytest.fixture
def df_with_data():
    return pd.DataFrame(
        {
            "Дата платежа": pd.to_datetime(["2021-12-01", "2021-12-05", "2021-11-30"]),
            "Сумма операции": [-237.0, -415.5, -90.0],
            "Описание": ["Оплата телефона +7 912 345-67-89", "Такси", "Пополнение"],
        }
    )


@patch("src.services.read_excel")
def test_get_transactions_filters_by_month(mock_read_excel, df_with_data):
    mock_read_excel.return_value = df_with_data
    result = get_transactions("2021-12", "fake_file.xlsx")
    assert len(result) == 2
    assert result[0]["amount"] == 237.0
    assert result[0]["date"] == "2021-12-01"


@pytest.mark.parametrize("limit,expected", [(10, 17.5), (50, 57.0)])
def test_investment_bank(fake_transactions, limit, expected):
    result = investment_bank("2021-12", fake_transactions, limit)
    assert round(result, 2) == expected


@patch("src.services.read_excel")
def test_find_phone_transactions_success(mock_read_excel, df_with_data):
    mock_read_excel.return_value = df_with_data
    json_result = find_phone_transactions("fake.xlsx")
    assert "+7 912 345-67-89" in json_result
    assert "Такси" not in json_result


@patch("src.services.read_excel")
def test_find_phone_transactions_empty(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame()
    result = find_phone_transactions("empty.xlsx")
    assert result == json.dumps({"transactions": []}, ensure_ascii=False, indent=2)


@patch("src.services.read_excel")
def test_find_phone_transactions_no_description_column(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame({"Сумма операции": [-500]})
    result = find_phone_transactions("nodata.xlsx")
    assert result == json.dumps({"transactions": []}, ensure_ascii=False, indent=2)
