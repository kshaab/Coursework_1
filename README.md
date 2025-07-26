# Analysis of banking operations

### Приложение для анализа банковских операций. 

### Проект завершен.

## Содержание 

- [Использование](#использование)
- [Разработка](#разработка)
- [Зависимости](#зависимости)
- [Тестирование](#тестирование)
- [Автор](#автор)


## Использование
Клонируйте репозиторий: 
```bash
git clone https://github.com/kshaab/Coursework_1
cd crswrk_1
```
Установите зависимости и активируйте виртуальное окружение: 
poetry install
poetry shell

Запустите файл: 
python src/<имя файла>.py


## Разработка

## Основные функции
### Utils
- ### `read_excel(excel_file: str)` 
Читает данные из файла с операциями.

read_excel(excel_data)

- ### `read_json(json_file: str)` 
Читает файл с настройками пользователя.

read_json(json_data)

- ### `filter_by_date(df: pd.DataFrame, date: Union[str, pd.Timestamp])`
Фильтрует диапазон от начала месяца до заданной даты включительно.

filter_by_date(df, date)

- ### `view_cards_info(df: pd.DataFrame, date: Union[str, pd.Timestamp])`
Выводит данные по картам.

view_cards_info(read_data, required_date)
### {'last_digits': '4556', 'total_spent': 703.0, 'cashback': 7}

- ### `search_top(df: pd.DataFrame, date: Union[str, pd.Timestamp])`
Собирает топ-5 операций по сумме платежа. 

search_top(read_data, required_date)
### {"date": "2020-11-02", "amount": 703.0, "category": "Аптеки", "description": "Аптека Вита"}, {"date": "2020-11-05", "amount": 462.0, "category": "Супермаркеты", "description": "WILDBERRIES"} и т.д.

- ### `view_exchange_rate(settings: Dict[str, Any])`
Выводит текущий курс валют, в зависимости от настроенных валют пользователя.

view_exchange_rate(read)
### [{'currency': 'USD', 'rate': 79.38}, {'currency': 'EUR', 'rate': 93.25}]

- ### `view_stock_prices(settings: Dict[str, Any])`
Выводит стоимость акций в зависимости от настроенных акций пользователя

view_stock_prices(read)
### {"stock": "AAPL", "price": 213.88}, {"stock": "AMZN", "price": 231.44}

### Views
- ### `greeting` 
Отображает приветствие в зависимости от времени суток. 

current_time = 13:00:00 
greeting()
### 'Добрый день'

- ### `view_homepage` 
Объединяет работу вспомогательных функций из utils.py и возвращает JSON-ответ.

view_homepage(input_date)

### Services
- ### `get_transactions(month: str, excel_file: str)` 
Собирает транзакции из файла в список словарей.

get_transactions("2021-11", excel_data)

- ### `investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int)` 
Возвращает сумму, отложенную в Инвесткопилку. 

investment_bank("2021-11", transactions, 10)
### 653.71

- ### `find_phone_transactions(excel_file: str)`
Находит операции в файле, содержащие номер телефона в описании.

find_phone_transactions(excel_data)
### {"transactions": [{"date": "19.11.2021", "amount": 200.0, "description": "Тинькофф Мобайл +7 995 555-55-55"}, {"date": "19.11.2021", "amount": 200.0, "description": "Тинькофф Мобайл +7 995 555-55-55"} и т.д.

### Reports
- ### `save_report_to_file(file: Optional[str] = None)`
Декоратор для записи отчета в файл.

@save_report_to_file("spending_report.json")

- ### `spending_by_category(t: pd.DataFrame, category: str, date: Optional[str] = None)`
Возвращает траты по заданной категории за последние три месяца от переданной даты.

spending_by_category(transactions, "Транспорт", "2019-11-16")
### {"категория": "Транспорт", "с": "2019-08-18", "по": "2019-11-16", "трат всего": 7795.43, "транзакций": 49}

### Main
- ### `main()`
Объединяет работу модулей в единую программу.

main()

## Зависимости
Управление зависимостями осуществляется через Poetry (pyproject.toml).


## Тестирование
В проекте используется фреймворк pytest для запуска тестов.

Запуск тестов:
```bash
pytest tests/ -v
```

## Автор
[Ксения](https://github.com/kshaab)
