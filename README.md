# CSV Filter and Aggregator

Фильтрация и агрегация CSV-файлов.

# Установка

Python 3.7+

```bash

# Примеры запуска
python main.py --file products.csv --where "price>500"
python main.py --file products.csv --aggregate "rating=avg"
python main.py --file products.csv --order-by "price=desc"

# Тестирование
pytest test_main.py
```
