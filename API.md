# API

## USERS

1. **Авторизация пользователя**  
   ***URL: `POST http://127.0.0.1:8000/u/api/login/`***

   **Описание:**  
   Принимает `email` и `password`, выполняет аутентификацию пользователя и возвращает `access_token` и `refresh_token` в теле ответа. Токены должны быть использованы в заголовках `Authorization` для дальнейших запросов.

   **Тело запроса:**

   ```json
   {
     "email": "example@domain.com",
     "password": "your_password"
   }
   ```

    **Пример запроса:**


    ```http
    POST http://127.0.0.1:8000/u/api/login/
    Content-Type: application/json

    {
      "email": "bajenchik@smradnik.com",
      "password": "pwd1488"
    }
    ```
    **Ответ при успешной аутентификации (статус 200):**


    ```json
    {
      "access_token": "<ваш access_token>",
      "refresh_token": "<ваш refresh_token>",
      "role": "user_role"
    }
    ```
    **Ошибки:**
    ---
    `401 Unauthorized`: Неверные учетные данные.

    `403 Forbidden`: Суперпользователь не может авторизоваться через этот эндпоинт.

    **Примечание:**

    Токены (`access_token` и `refresh_token`) должны быть переданы в заголовке `Authorization` в следующем формате:

    `Authorization: Bearer <access_token>` для запросов, требующих аутентификации.

    ---


2. **Тестовый публичный эндпоинт**
    ***URL: GET http://127.0.0.1:8000/u/api/test/***

    **Описание:**
  
    Публичный эндпоинт, доступный без авторизации. Возвращает сообщение для тестирования доступности API.

    **Пример запроса:**

    ```http
    GET http://127.0.0.1:8000/u/api/test/
    Content-Type: application/json
    ```
    
    Ответ (статус 200):

    ```json
    {
      "message": "Successful test"
    }
    ```

3. **Защищенный тестовый эндпоинт**

    ***URL: GET http://127.0.0.1:8000/u/api/secure_test/***

    **Описание:**

    Защищенный эндпоинт, доступный только для аутентифицированных пользователей. Требует, чтобы `access_token` был передан через заголовок `Authorization` как `Bearer токен`.

    **Пример запроса:**

    ```http
    GET http://127.0.0.1:8000/u/api/secure_test/
    Content-Type: application/json
    Authorization: Bearer <ваш access_token>
    ```
    **Ответ при успешной аутентификации (статус 200):**

    ```json
    {
      "message": "Successful secure test"
    }
    ```
    **Ошибки:**

    ---

    `401 Unauthorized`: Отсутствует или истек `access_token`.

    Обновление токена доступа (Refresh)

    ***URL: POST http://127.0.0.1:8000/u/api/refresh/***

    **Описание:**

    Обновляет `access_token` и `refresh_token`, используя текущий `refresh_token`, который передается в теле запроса. Возвращает новые токены в теле ответа.

    **Пример запроса:**

    ```http
    POST http://127.0.0.1:8000/u/api/refresh/
    Content-Type: application/json
    Authorization: Bearer <ваш refresh_token>
    ```
    **Ответ при успешном обновлении (статус 200):**

    ```json
    {
      "detail": "New tokens have been sent"
    }
    ```
    ---

    **Ошибки:**

    `400 Bad Request`: Отсутствует `refresh_token` или токен невалиден.

    `403 Forbidden`: Попытка обновить токены для суперпользователя.

    **Общие примечания:**

    **Токены:**

    `access_token` используется для авторизации защищенных эндпоинтов. Он должен быть передан в заголовке `Authorization` в формате: `Authorization: Bearer <access_token>`

    `refresh_token` используется для обновления `access_token`. Он также передается в заголовке `Authorization` в формате:
    `Authorization: Bearer <refresh_token>.`

    ---

4. **Тест с ограничением по роли (только для администраторов)**
    ***URL: GET http://127.0.0.1:8000/u/api/test_role/***

    **Описание:**

    Этот эндпоинт доступен только пользователям с ролью `ADMIN`. При успешной авторизации возвращает сообщение, приветствующее пользователя и показывающее его роль.
    Требует передачи действительного `access_token` в заголовке Authorization как Bearer токен.

    **Пример запроса:**

    ```http
    GET http://127.0.0.1:8000/u/api/test_role/
    Content-Type: application/json
    Authorization: Bearer <ваш access_token>
    ```
    **Ответ (статус 200):**
    ```json
    {
      "message": "Hello, <user_first_name>! Your role: ADMIN This was a test."
    }
    ```
    **Ошибки:**

    `401 Unauthorized`: Отсутствует или истек `access_token`.

    `403 Forbidden`: Пользователь не имеет права выполнять этот запрос (если у него нет роли `ADMIN`).

    **Безопасность токенов:**
    Токены должны передаваться через защищенные каналы (например, через HTTPS).
    В production режиме важно использовать флаг secure для передачи токенов через HTTPS, чтобы предотвратить перехват токенов.

    **Ошибки:**
    ---
    В случае недействительных токенов API возвращает статус-коды:

    `401 Unauthorized`: Неверные или отсутствующие токены.

    `400 Bad Request`: Невалидные токены.

    `403 Forbidden`: Попытка выполнения операции для суперпользователя, которая не разрешена для обычных пользователей.
    
    ---
