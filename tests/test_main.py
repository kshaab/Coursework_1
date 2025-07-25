from unittest.mock import patch, MagicMock


@patch("builtins.print")
@patch("src.main.pd.read_excel")
@patch("src.main.spending_by_category")
@patch("src.main.find_phone_transactions")
@patch("src.main.investment_bank")
@patch("src.main.get_transactions")
@patch("src.main.view_homepage")
def test_main_success(
    mock_view_homepage,
    mock_get_transactions,
    mock_investment_bank,
    mock_find_phone_transactions,
    mock_spending_by_category,
    mock_read_excel,
    mock_print,
):

    mock_view_homepage.return_value = {"greeting": "Добрый день"}
    mock_get_transactions.return_value = [{"date": "2021-12-01", "amount": 100}]
    mock_investment_bank.return_value = 300.0
    mock_find_phone_transactions.return_value = '{"transactions": []}'
    mock_spending_by_category.return_value = {
        "категория": "Транспорт",
        "трат всего": 1000,
        "транзакций": 5,
    }
    mock_read_excel.return_value = MagicMock()

    from src.main import main

    main()

    mock_view_homepage.assert_called_once()
    mock_get_transactions.assert_called_once()
    mock_investment_bank.assert_called_once()
    mock_find_phone_transactions.assert_called_once()
    mock_spending_by_category.assert_called_once()
    mock_print.assert_any_call("Главная страница:")
    mock_print.assert_any_call("Инвесткопилка:")
    mock_print.assert_any_call("Телефонные транзакции:")
    mock_print.assert_any_call("Отчет по категории:")
