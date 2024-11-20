# API
## USERS
1. **Авторизация пользователя**\
URL: ***POST http://127.0.0.1:8000/u/api/login/***

__Описание:__ Принимает email и пароль, выполняет аутентификацию и возвращает user_id и role. Устанавливает токены (access_token и refresh_token) в cookies.

Тело запроса:

```json
{
  "email": "example@domain.com",
  "password": "your_password"
}
```
Пример запроса:

```http
POST http://127.0.0.1:8000/u/api/login/
Content-Type: application/json

{
  "email": "bajenchik@smradnik.com",
  "password": "pwd1488"
}
```
Ответ при успешной аутентификации (статус 200):

```json
{
  "user_id": 123,
  "role": "user_role"
}
```
__Cookies:__ В ответе API устанавливает access_token и refresh_token в cookies. Эти токены используются для дальнейших запросов, требующих аутентификации.

__Ошибки:__

401 Unauthorized: Неверные учетные данные.
2. **Тестовый публичный эндпоинт**\
URL: ***GET http://127.0.0.1:8000/u/api/test/***

__Описание:__ Публичный эндпоинт, доступный без авторизации. Возвращает сообщение для тестирования доступности API.

Пример запроса:

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
3. **Защищенный тестовый эндпоинт**\
URL: ***GET http://127.0.0.1:8000/u/api/secure_test/***

__Описание:__ Защищенный эндпоинт, доступный только для аутентифицированных пользователей. Требует access_token в cookies.

Пример запроса:

```http
GET http://127.0.0.1:8000/u/api/secure_test/
Content-Type: application/json
Cookie: access_token=<ваш access_token>
```
Ответ (статус 200):

```json
{
  "message": "Successful secure test"
}
```
__Ошибки:__

401 Unauthorized: Отсутствует или истек access_token.
4. **Обновление токена доступа (Refresh)**\
URL: ***POST http://127.0.0.1:8000/u/api/refresh/***

__Описание:__ Обновляет access_token и refresh_token, используя текущий refresh_token из cookies. Возвращает сообщение о том, что новые токены были установлены.

Пример запроса:

```http
POST http://127.0.0.1:8000/u/api/refresh/
Content-Type: application/json
Cookie: refresh_token=<ваш refresh_token>
```
Ответ при успешном обновлении (статус 200):

```json
{
  "detail": "New tokens have been sent"
}
```
__Cookies:__ В ответе API устанавливает новые access_token и refresh_token в cookies.

__Ошибки:__

400 Bad Request: Отсутствует refresh_token в cookies или предоставлен невалидный токен.
## Общие примечания:
### Токены:

__access_token__ используется для авторизации защищенных эндпоинтов. Передавайте его в __cookies__.\
__refresh_token__ используется для обновления __access_token__ и также передается через __cookies__.
### Безопасность cookies:

В __production__ режиме токены передаются с флагами __httponly__ и __secure__, что делает их доступными только через HTTPS и защищенными от JavaScript-доступа.\
__Ошибки:__ В случае недействительных токенов API возвращает статус-коды 401 (Unauthorized) или 400 (Bad Request), с пояснениями в __detail__.