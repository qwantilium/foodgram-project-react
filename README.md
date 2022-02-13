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
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/qwantilium/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Запуск приложения в конейнере ТУТОРИАЛ
Создать образ приложения ИЗ КОРНЯ ПРОЕКТА:
```
docker build -t 'название образа' .
```
Собрать и запустить все образы вместе с NGINX и GUNICORN:
```
docker-compose up -d
```
Теперь проект доступен по адресу http://127.0.0.1/

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
Войдите в админку по адресу http://localhost/admin/
Создайте одну-две записи объектов.

Создать резервную копию базы данных
```
docker-compose exec backend  python manage.py dumpdata > fixtures.json
```