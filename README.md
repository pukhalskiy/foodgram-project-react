# Foodgram

## Технологии

- Python 3.9
- Django 4.2.5
- Django REST framework 3.14
- Nginx
- Docker
- Postgres

## http://foodgram14.ddns.net/


### Для развертывания проекта выполните следующие действия:

- Клонируйте проект по SSH:

```text
git clone git@github.com:perineum14/foodgram-project-react.git
```

- Подключитесь к вашему серверу:

```text
ssh <server user>@<server IP>
```

- Установите Docker на сервер

```text
sudo apt install docker.io
```

- Перейдите в директорию проекта и переименуйте файл .emv.example в .env:

```text
mv .env.example.env .env
```

- Заполните .env:

```text
POSTGRES_USER=<django_user>
POSTGRES_PASSWORD=<mysecretpassword>
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<secret_key>
DEBUG='False'
HOSTS=<hosts>
TESTING='False'
```

- Запустите docker compose из директории /infra внутри проекта:

```text
sudo docker compose up --build -d
```

- Соберите статику:
```text
docker exec infra-backend-1 python manage.py collectstatic
```

- Скопируйте статику:
```text
docker exec infra-backend-1 cp -r /app/static/. /backend_static/static/
```

- Сделайте миграции:
```text
docker exec infra-backend-1 python manage.py migrate
```

- Создайте суперпользователя:
```text
docker exec -it infra-backend-1 python manage.py createsuperuser
```

- Перейдите в папку бекенда:
```text
cd backend/foodgram/
```

- Скопируйте данные для БД:
```text
docker cp ingr.json infra-backend-1:/app/ingr.json
docker cp tags.json infra-backend-1:/app/tags.json
```

- Загрузите данные для БД:
```text
docker exec infra-backend-1 python manage.py loaddata ingr.json
docker exec infra-backend-1 python manage.py loaddata tags.json
```