# Stripe Shop 

## О проекте  
Интернет-магазин на Django с интеграцией Stripe (тестовый режим).  
Поддержка создания товаров, заказов, скидок и налогов с мультивалютной оплатой.

## Функционал  
- Модель `Item`: название, описание, цена в центах, валюта, фото.  
- Модель `Order`: заказ с множеством товаров, применением скидок и налогов.  
- Модели `Discount` и `Tax` для учета в заказах и Stripe Checkout.  
- REST API для создания Stripe Checkout Session.  
- Админка для управления товарами, заказами, скидками и налогами.

## Библиотеки  
- Python 3.11+  
- Django 4.x  
- stripe==5.x  
- python-dotenv  

## Быстрый запуск  

1. Клонировать репозиторий:  
git clone https://github.com/NikitosZ112/stripe_shop_test1.git
cd stripe_shop

2. Создать и активировать виртуальное окружение:  
    python -m venv venv

    Windows PowerShell
    venv\Scripts\Activate.ps1

    Linux/macOS
    source venv/bin/activate

3. Установить зависимости:  
    pip install -r requirements.txt

4. Создать `.env` с переменными:  

    STRIPE_SECRET_KEY=
    STRIPE_PUBLISHABLE_KEY=

5. Выполнить миграции:  
    python manage.py migrate


6. Запустить сервер:  
    python manage.py runserver


## Админ-панель  
    - URL: `http://127.0.0.1:8000/admin/`  
    - Логин: `nik`  
    - Пароль: `testtest`  

    Управление товарами, заказами, скидками, налогами.

## Использование  
    - Добавлять товары через админку.  
    - Просмотр товаров — `/items/` или `/item/<id>/`.  
    - Оплата через Stripe Checkout.

    ---

    Проект ориентирован на тестирование и демонстрацию интеграции Stripe с Django.