# API

Конечные точки users
--------------

## 1\. Эндпоинты аутентификации

### `POST /login/`

-   **Описание**: Аутентифицирует пользователя по электронной почте и паролю.

-   **Разрешения**: Доступен для всех (`AllowAny`).

-   **Тело запроса**:

```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
```
-   **Пример запроса**:

``` http
    POST http://127.0.0.1:8000/u/api/login/
    Content-Type: application/json
    X-CSRFToken: {ваш_csrf_токен}

    {
      "email": "user@example.com",
      "password": "password123"
    }
```

-   **Ответы**:

    -   `200 OK`: Успешный вход, возвращает роль пользователя.

```json
        {
          "message": "Successfully logged in!",
          "role": "USER"
        }
```
-   401 Unauthorized`: Неверные учетные данные.

```json
        {
          "detail": "Invalid credentials"
        }
```
### `POST /logout/`

-   **Описание**: Завершает сеанс текущего пользователя, удаляя сессию.

-   **Разрешения**: Только для аутентифицированных пользователей.

-   **Пример запроса**:

```http
    POST http://127.0.0.1:8000/u/api/logout/
    Content-Type: application/json
    X-CSRFToken: {ваш_csrf_токен}

    {}
```
-   **Ответ**:

    -   `200 OK`: Успешный выход из системы.

```json
        {
          "detail": "Successfully logged out."
        }
```
* * * * *

## 2\. Тестовые эндпоинты

### `GET /test/`

-   **Описание**: Простая тестовая точка, чтобы проверить доступность API.

-   **Разрешения**: Доступен для всех (`AllowAny`).

-   **Пример запроса**:

```http
    GET http://127.0.0.1:8000/u/api/test/
    Content-Type: application/json

    {}
```
-   **Ответ**:

    -   `200 OK`: Подтверждает успешный ответ API.

```json
        {
          "message": "Successful test"
        }
```
### `GET /secure_test/`

-   **Описание**: Тестовый эндпоинт, требующий авторизации пользователя.

-   **Разрешения**: Только для аутентифицированных пользователей.

-   **Пример запроса**:

```http
    GET http://127.0.0.1:8000/u/api/secure_test/
    Content-Type: application/json

    {}
```
-   **Ответ**:

    -   `200 OK`: Подтверждает успешный ответ API.

```json
        {
          "message": "Successful secure test"
        }
```
### `GET /role_test/`

-   **Описание**: Тестовая точка для проверки ролей пользователя. Доступно только для `ADMIN` роли.

-   **Разрешения**: Требуется любая роль кроме `DUMMY`.

-   **Пример запроса**:

```http
    GET http://127.0.0.1:8000/u/api/role_test/
    Content-Type: application/json

    {}
```
-   **Ответ**:

    -   `200 OK`: Возвращает приветствие с именем пользователя и его ролью.

```json
        {
          "message": "Hello, John! Your role: ADMIN. This was a test."
        }
```
* * * * *

### 3\. `UserViewSet` для модели `User`

### Базовая точка: `/users/`

`UserViewSet` поддерживает стандартные CRUD-операции с ограничениями по ролям.

-   **Разрешения**: Только для аутентифицированных пользователей (`IsAuthenticated`), с дополнительными ограничениями по ролям.

### `GET /users/`

-   **Описание**: Получает список всех пользователей.

-   **Разрешения**: Ограничивается ролями, указанными в `only_for_self`.

-   **Пример запроса**:

```http
    GET http://127.0.0.1:8000/u/api/users/
    Content-Type: application/json

    {}
```
-   **Ответ**:

    -   `200 OK`: Возвращает список пользователей.

### `GET /users/{id}/`

-   **Описание**: Получает информацию о конкретном пользователе по его ID.

-   **Разрешения**: Ограничивается для ролей `STAGE_MANAGER` и `PROJECT_MANAGER` только для доступа к собственным данным, без ограничений для более высоких ролей.

-   **Пример запроса**:

```http
    GET http://127.0.0.1:8000/u/api/users/{id}/
    Content-Type: application/json

    {}
```
-   **Ответ**:

    -   `200 OK`: Возвращает данные пользователя.

### `POST /users/`

-   **Описание**: Создает нового пользователя.

-   **Разрешения**: Только для роли `ADMIN`.

-   **Тело запроса**: Поля из `UserCreateSerializer`.

-   **Пример запроса**:

```http
    POST http://127.0.0.1:8000/u/api/users/
    Content-Type: application/json
    X-CSRFToken: {ваш_csrf_токен}

    {
      "email": "newuser@example.com",
      "password": "newpassword123",
      "first_name": "John",
      "last_name": "Doe",
      "phone": "+78005553535",
      "passport": "7778 677999"
    }
```
-   **Ответ**:

    -   `201 Created`: Пользователь успешно создан.

### `PUT /users/{id}/` и `PATCH /users/{id}/`

-   **Описание**: Обновляет информацию о существующем пользователе.

-   **Разрешения**: Только для роли `ADMIN`.

-   **Тело запроса**: Поля из `UserUpdateSerializer`.

-   **Пример запроса**:

```http
    PUT http://127.0.0.1:8000/u/api/users/{id}/
    Content-Type: application/json
    X-CSRFToken: {ваш_csrf_токен}

    {
      "first_name": "UpdatedJohn",
      "last_name": "Doe"
    }
```
-   **Ответ**:

    -   `200 OK`: Пользователь успешно обновлен.

### `DELETE /users/{id}/`

-   **Описание**: Удаление пользователя отключено и вызывает ошибку `MethodNotAllowed`.

-   **Разрешения**: Отключено (метод не разрешен).

-   **Пример запроса**:

```http
    DELETE http://127.0.0.1:8000/u/api/users/{id}/
    Content-Type: application/json

    {}
```
-   **Ответ**:

    -   `405 Method Not Allowed`: Удаление пользователя не разрешено.

* * * * *

## Конечные точки projects

* * * * *

## Конечные точки contractors

* * * * *



## Как получить CSRF и отправить в headers

- Пример реализации на JS

```JavaScript
function getCSRFToken() {
    if (!document.cookie) {
        return null;
    }
    const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith('csrftoken' + '='));

    if (xsrfCookies.length === 0) {
        return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}
```
