# Спецификация API

## Общая информация

Серверная часть предоставляет REST API. Формат обмена данными — JSON. Документация OpenAPI автоматически доступна после запуска приложения по адресу:

```text
http://127.0.0.1:8000/docs
```

Базовый адрес при локальном запуске:

```text
http://127.0.0.1:8000
```

## Авторизация

Для защищенных методов используется JWT access token. Токен передается в заголовке:

```text
Authorization: Bearer <access_token>
```

## Служебный endpoint

### GET /health

Проверка работоспособности приложения.

Ответ:

```json
{
  "status": "ok"
}
```

## Auth

### POST /auth/register

Регистрация пользователя.

Пример запроса:

```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "Иван",
  "last_name": "Иванов",
  "phone": "+7 999 123-45-67"
}
```

Результат:

- создается пользователь;
- создается профиль;
- создается бонусная карта;
- создается уникальный реферальный код.

### POST /auth/login

Вход пользователя.

Пример запроса:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Пример ответа:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

## Users

### GET /users/me

Получение данных текущего пользователя.

Требуется авторизация.

## Menu

### GET /menu/categories

Получение списка категорий меню.

### GET /menu/products

Получение списка доступных товаров.

### GET /menu/products/{product_id}

Получение информации о товаре по идентификатору.

## Admin Menu

### POST /admin/categories

Создание категории.

Пример запроса:

```json
{
  "name": "Кофе",
  "description": "Кофейные напитки"
}
```

### POST /admin/products

Создание товара.

Пример запроса:

```json
{
  "category_id": 1,
  "name": "Латте",
  "description": "Кофе с молоком",
  "price": 250,
  "image_url": "https://example.com/latte.jpg",
  "calories": 180,
  "weight": null,
  "volume": 300,
  "is_available": true,
  "is_preorder_available": true
}
```

### PATCH /admin/products/{product_id}

Изменение товара.

### DELETE /admin/products/{product_id}

Удаление товара.

## Orders

### POST /orders

Создание заказа.

Требуется авторизация.

Пример запроса:

```json
{
  "order_type": "preorder",
  "pickup_time": "2026-05-01T12:00:00",
  "bonus_used": 0,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

### GET /orders/my

Получение заказов текущего пользователя.

### GET /orders/{order_id}

Получение заказа по идентификатору.

### PATCH /orders/{order_id}/cancel

Отмена заказа пользователем.

## Admin Orders

### GET /admin/orders

Получение всех заказов.

### PATCH /admin/orders/{order_id}/status

Изменение статуса заказа.

Пример запроса:

```json
{
  "status": "completed"
}
```

При переводе заказа в статус `completed` запускается начисление бонусов и проверка реферальной программы.

## Loyalty

### GET /loyalty/card

Получение бонусной карты текущего пользователя.

Требуется авторизация.

### GET /loyalty/transactions

Получение истории бонусных операций текущего пользователя.

Требуется авторизация.

## Referrals

### GET /referrals/my-code

Получение собственного реферального кода.

### POST /referrals/apply-code

Применение реферального кода.

Пример запроса:

```json
{
  "referral_code": "ABC12345"
}
```

### GET /referrals/my-invited-users

Получение списка приглашенных пользователей.

## Promotions

### GET /promotions

Получение списка активных акций.

### GET /promotions/{promotion_id}

Получение акции по идентификатору.

## Admin Promotions

### POST /admin/promotions

Создание акции.

Пример запроса:

```json
{
  "title": "Весенняя акция",
  "description": "Скидка на кофейные напитки",
  "discount_percent": 15,
  "start_date": "2026-01-01",
  "end_date": "2026-12-31",
  "is_active": true
}
```

### PATCH /admin/promotions/{promotion_id}

Изменение акции.

### DELETE /admin/promotions/{promotion_id}

Удаление акции.

## Coffee Shop

### GET /coffee-shop/info

Получение полной информации о кофейне.

### GET /coffee-shop/location

Получение информации для отображения местоположения кофейни на карте.

## Admin Coffee Shop

### PATCH /admin/coffee-shop

Создание или обновление информации о кофейне.

Пример запроса:

```json
{
  "name": "Brew House",
  "address": "Main Street 1",
  "latitude": 55.751244,
  "longitude": 37.618423,
  "phone": "+7 999 123-45-67",
  "working_hours": "08:00-22:00",
  "description": "Уютная кофейня со свежей выпечкой и авторским кофе.",
  "image_url": "https://example.com/coffee-shop.jpg",
  "social_links": {
    "instagram": "https://instagram.com/brewhouse"
  }
}
```

## Коды ответов

Основные HTTP-коды:

- `200 OK` — успешное получение или изменение данных;
- `201 Created` — успешное создание записи;
- `204 No Content` — успешное удаление;
- `400 Bad Request` — ошибка в данных запроса;
- `401 Unauthorized` — отсутствует или некорректен токен;
- `404 Not Found` — запись не найдена;
- `422 Unprocessable Entity` — ошибка валидации.
