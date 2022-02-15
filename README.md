# praktikum_new_diplom
![Status of build](https://github.com/qwantilium/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)

ip server 51.250.31.207

### Шаблон .env файла:
```
DB_ENGINE='СУБД на выбор'
DB_NAME='Имя базы данных'
POSTGRES_USER='имя пользователя'
POSTGRES_PASSWORD='пароль пользователя'
DB_HOST='хост'
DB_PORT='порт'
```
### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/qwantilium/foodgram-project-react.git
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```
Обновить pip
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Запуск приложения в конейнере ТУТОРИАЛ
Перейти в нужную директорию
```
cd foodgram-project-react/infra/
```
Создать образ приложения ИЗ КОРНЯ ПРОЕКТА:
```
docker build -t 'название образа' .
```
Собрать и запустить все образы вместе с NGINX и GUNICORN:
```
docker-compose up -d
```
Теперь проект доступен по адресу localhost

Остановить все образы:
```
docker-compose down
```

### Собрать и заполнить базу данных
Выполните миграции.
```
docker-compose exec backend python manage.py migrate --noinput
```
Создайте суперпользователя.
```
docker-compose exec backend python manage.py createsuperuser
```
Собрать статику
```
docker-compose exec backend  python manage.py collectstatic --no-input 
```
Загрузить в базу список ингридентов
```
docker-compose exec backend  python manage.py load_csv
```
или
```
docker-compose exec web python3 manage.py load_json_data
```
Войдите в админку по адресу http://localhost/admin/
Создайте одну-две записи объектов.

Создать резервную копию базы данных
```
docker-compose exec backend  python manage.py dumpdata > fixtures.json
```