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

### Базовая точка `/p/api/`

Этот раздел описывает API эндпоинты для управления проектами, файлами, этапами и назначениями. Все эндпоинты ниже требуют аутентификации (IsAuthenticated). Дополнительные ограничения по ролям указаны для каждого эндпоинта. `@assignment_required` означает, что пользователь должен быть назначен на проект (статус `ACTIVE` или `FREEZED`) для доступа к ресурсу.


## 1. `ProjectViewSet`

Этот `ViewSet` управляет ресурсом `Project` и предоставляет стандартные CRUD операции с ограничениями по ролям и назначению.


### `/p/api/projects/`

-   **Описание:** Получает список всех проектов.

-   **Разрешения:** `role_required(['ADMIN', 'PROJECT_MANAGER', 'RULER']), assignment_required(['ACTIVE', 'FREEZED'])`

-   **Пример запроса:**
```http
    GET http://127.0.0.1:8000/p/api/projects/ 
    Content-Type: application/json

    {}
```


-   **Ответ:**

    -   * `200 OK`: Возвращает список проектов (сериализованный с помощью `ReadProjectSerializer`).


### `/p/api/projects/{id}/`

-   **Описание:** Получает информацию о конкретном проекте по его ID.

-   **Разрешения:** `role_required(['ADMIN', 'PROJECT_MANAGER', 'RULER']), assignment_required(['ACTIVE', 'FREEZED'])`

-   **Пример запроса:**
```http
    GET http://127.0.0.1:8000/p/api/projects/{id}/ 
    Content-Type: application/json

    {}
```

-   **Ответ:**

    -   * `200 OK`: Возвращает данные проекта (сериализованный с помощью `ReadProjectSerializer`).
    -   * `404 Not Found`: Проект не найден.


### `/p/api/projects/`

-   **Описание:** Создает новый проект.

-   **Разрешения:** `role_required(['ADMIN', 'PROJECT_MANAGER']), assignment_required(['ACTIVE'])`

-   **Пример запроса:**
```http
    POST http://127.0.0.1:8000/p/api/projects/ 
    Content-Type: application/json \
    X-CSRFToken: {ваш_csrf_токен} 
    
    { 
        // Данные проекта согласно CreateProjectSerializer 
    }
```


-   **Ответ:**

    -   * `201 Created`: Проект успешно создан.
    -   * `400 Bad Request`: Ошибка валидации данных.
    -   * `403 Forbidden`: CSRF токен неверный или отсутствует.


### `/p/api/projects/{id}/` (PUT/PATCH)

-   **Описание:** Обновляет информацию о существующем проекте.

-   **Разрешения:** `role_required(['ADMIN', 'PROJECT_MANAGER']), assignment_required(['ACTIVE'])`

-   **Пример запроса (PUT):**
```http
    PUT http://127.0.0.1:8000/p/api/projects/{id}/ 
    Content-Type: application/json 
    X-CSRFToken: {ваш_csrf_токен} 

    { 
        // Данные проекта согласно UpdateProjectSerializer 
    }
```


-   **Ответ:**

    -   * `200 OK`: Проект успешно обновлен.
    -   * `400 Bad Request`: Ошибка валидации данных.
    -   * `404 Not Found`: Проект не найден.
    -   * `403 Forbidden`: CSRF токен неверный или отсутствует.


### `/p/api/projects/{id}/` (DELETE)

-   **Описание:** Удаление проекта отключено.

-   **Разрешения:** Запрещено.

-   **Ответ:**

    -   * `405 Method Not Allowed`: Удаление проекта не разрешено.


## 2. `FileViewSet`, `StageViewSet`, `ProjectAssignmentViewSet`, `StageAssignmentViewSet`

Эти `ViewSet` управляют файлами, этапами и назначениями к проектам и этапам соответственно. Документация для каждого из них аналогична `ProjectViewSet`, но с соответствующими моделями, сериализаторами и ограничениями по ролям.  Базовые пути: `/p/api/files/`, `/p/api/stages/`, `/p/api/project_assignments/`, `/p/api/stage_assignments/`.


## 3. `/p/api/test_assign/<uuid:project_id>/<uuid:stage_id>/`

-   **Описание:** Тестовый эндпоинт для проверки разрешений на основе роли и назначения. Возвращает приветственное сообщение пользователю, если доступ разрешен.

-   **Разрешения:** `role_required(['ADMIN']), assignment_required(['ACTIVE', 'FREEZED'])`

-   **Пример запроса:**
```http
    GET http://127.0.0.1:8000/p/api/test_assign/{project_id}/{stage_id}/

    {}
```
-   **Примечание:** `uuid:project_id` и `uuid:stage_id` указывают, что `project_id` и `stage_id` должны быть UUID.
* * * * *
## Конечные точки contractors

### Базовая точка: `/c/api/` 

Все эндпоинты ниже требуют аутентификации (IsAuthenticated). Дополнительные ограничения по ролям указаны для каждого эндпоинта.

Этот раздел API описывает три типа контрагентов: `SubContractors`, `GovernmentalCompanies`, и `ContactFaces`.

## 1. SubContractorViewSet

Управляет ресурсом SubContractor.

### GET `/c/api/projects/`

-   **Описание:** Получает список всех субподрядчиков.

-   **Разрешения:** role_required(['ADMIN', 'PROJECT_MANAGER', 'RULER', 'STAGE_MANAGER'])

-   **Пример запроса:**

```http
    GET http://127.0.0.1:8000/c/api/projects/ 
    Content-Type: application/json

    {}
```

-   **Ответ:**

    -   * 200 OK: Возвращает список субподрядчиков (сериализованный с помощью SubContractorSerializer).

### GET `/c/api/projects/{id}/`

-   **Описание:** Получает информацию о конкретном субподрядчике по его ID.

-   **Разрешения:** role_required(['ADMIN', 'PROJECT_MANAGER', 'RULER', 'STAGE_MANAGER'])

-   **Пример запроса:**

```http
    GET http://127.0.0.1:8000/c/api/projects/{id}/ 
    Content-Type: application/json

    {}
```


-   **Ответ:**

    -   * 200 OK: Возвращает данные субподрядчика (сериализованный с помощью SubContractorSerializer).
    -   * 404 Not Found: Субподрядчик не найден.

### POST `/c/api/projects/`

-   **Описание:** Создает нового субподрядчика.

-   **Разрешения:** role_required(['ADMIN', 'PROJECT_MANAGER'])

-   **Пример запроса:**

```http
    POST http://127.0.0.1:8000/c/api/projects/ 
    Content-Type: application/json 
    X-CSRFToken: {ваш_csrf_токен} 

    { 
        // Данные субподрядчика согласно SubContractorSerializer 
    }
```

-   **Ответ:**

-   * 201 Created: Субподрядчик успешно создан.
-   * 400 Bad Request: Ошибка валидации данных.
-   * 403 Forbidden: CSRF токен неверный или отсутствует.

### PUT `/c/api/projects/{id}/` и PATCH `/c/api/projects/{id}/`

-   **Описание:** Обновляет информацию о существующем субподрядчике.

-   **Разрешения:** role_required(['ADMIN', 'PROJECT_MANAGER'])

-   **Пример запроса (PUT):**

```http
    PUT http://127.0.0.1:8000/c/api/projects/{id}/ 
    Content-Type: application/json 
    X-CSRFToken: {ваш_csrf_токен} 
    
    { 
        // Данные субподрядчика согласно SubContractorSerializer 
    }
```

-   **Ответ:**

    -   * 200 OK: Субподрядчик успешно обновлен.
    -   * 400 Bad Request: Ошибка валидации данных.
    -   * 404 Not Found: Субподрядчик не найден.
    -   * 403 Forbidden: CSRF токен неверный или отсутствует.

### DELETE `/c/api/projects/{id}/`

-   **Описание:** Удаление субподрядчика запрещено.

-   **Разрешения:** Запрещено.

-   **Ответ:**

    -   * 405 Method Not Allowed: Удаление субподрядчика не разрешено.

## 2. GovernmentalCompanyViewSet

Управляет ресурсом `GovernmentalCompany`. Документация аналогична `SubContractorViewSet`, за исключением модели и сериализатора (GovernmentalCompanySerializer). Базовый путь: `/c/api/governmental-companies/`.

## 3. ContactFaceViewSet

Управляет ресурсом ContactFace. Документация аналогична `SubContractorViewSet`, за исключением модели и сериализатора (ContactFaceSerializer). Базовый путь: `/c/api/contact-faces/`.
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
