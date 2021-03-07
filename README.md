# test-task-idaproject

Этот сервис позволяет загружать изображения с компьютера пользователя, или по ссылке, а затем изменять их размер.

## Инструкция по развёртыванию.

1. Скопируйте данный репозиторий к себе на компьютер.
```
git clone git@github.com:frolkit/test-task-idaproject.git
```
2. Создайте и активируйте виртуальное окружение.
```
cd test-task-idaproject
python -m venv venv
"venv/Scripts/activate.bat"
```
3. Установите зависимости.
```
pip install -r requirements.txt
```
4. Создайте и заполните файл .env в папке idaproject
```
copy .env.default .env 
```
5. Запустите тесты.
```
python manage.py test
```
6. Сделайте миграции и запустите проект.
```
python manage.py migrate
python manage.py runserver
```
7. Проект доступен по адресу 127:0.0.1:8000.

## Генерация SECRET_KEY для settings.py.
  1. SECRET_KEY можно получить по [ссылке](https://djecrety.ir/).
