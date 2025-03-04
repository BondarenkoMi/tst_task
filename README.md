Как запустить:

Клонируем репозиторий
```
git clone https://github.com/BondarenkoMi/tst_task
```
Создаем виртуальное окружение
```
python3 -m venv venv
```
Активируем виртуальное окружение
```
source venv/bin/activate
```
Устанавливаем зависимости
```
pip install -r requrements.txt
```
Запускаем тесты
```
pytest
```
Запускаем сервер разработки
```
python3 manage.py runserver
```
