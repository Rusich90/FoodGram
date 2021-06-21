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

Возможности:

* Публиковать, просматривать, изменять и удалять рецепты
* Подписываться на авторов
* Добавлять рецепты в избранное
* Добавлять рецепты в список покупок
* Выгружать ингридиенты из списка покупок в PDF файле для похода по магазинам =)

Проект доступен по адресу http://foodgram.rusich90.ru/

## Установка 
Клонируем репозиторий на локальную машину:

```$ git clone https://github.com/Rusich90/yatube.git```

 Создаем виртуальное окружение:
 
 ```$ python -m venv venv```
 
  Активируем виртуальное окружение
 
 ```$ source venv/Scripts/activate```
 
 Переходм в папку polls
 
 ```$ cd yatube/```
 
 Устанавливаем зависимости:

```$ pip install -r requirements.txt```

Создание и применение миграций:

```$ python manage.py makemigrations``` и ```$ python manage.py migrate```

Запускаем django сервер:

```$ python manage.py runserver```

Для подключения почтовой рассылки и мониторинга Sentry нужно создать файл .env (с секретными данными) в директории с settings.py и в самом settings.py раскомментировать настройки Sentry и почтового хоста.
