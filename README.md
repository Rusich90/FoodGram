# FoodGram - продуктовый помощник
## Описание


Для создания были использованы:

* Python
* Django
* PostgreSQL
* HTML
* JavaScript
* Linux
* Gunicorn, NGINX
* Docker, Docker-compose

Возможности:

* Публиковать, просматривать, изменять и удалять рецепты
* Подписываться на авторов
* Добавлять рецепты в избранное
* Добавлять рецепты в список покупок
* Выгружать ингридиенты из списка покупок в PDF файле для похода по магазинам =)

Проект доступен по адресу http://foodgram.rusich90.ru/

## Установка 
Клонируем репозиторий на локальную машину:

```$ git clone https://github.com/Rusich90/FoodGram.git```

 Переходим в папку проекта:
 
 ```$ cd FoodGram/foodgram```
 
  Создаём файл .env с секретными данными для доступа к Postgre 
 
 ```$ DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
      DB_NAME=postgres # имя базы данных
      POSTGRES_USER=<your_login> # логин для подключения к базе данных (установите свой)
      POSTGRES_PASSWORD=<your_password> # пароль для подключения к БД (установите свой)
      DB_HOST=db # название сервиса (контейнера)
      DB_PORT=5432 # порт для подключения к БД```
 
 Переходм в папку polls
 
 ```$ cd yatube/```
 
 Устанавливаем зависимости:

```$ pip install -r requirements.txt```

Создание и применение миграций:

```$ python manage.py makemigrations``` и ```$ python manage.py migrate```

Запускаем django сервер:

```$ python manage.py runserver```

Для подключения почтовой рассылки и мониторинга Sentry нужно создать файл .env (с секретными данными) в директории с settings.py и в самом settings.py раскомментировать настройки Sentry и почтового хоста.
