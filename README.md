# DATABASE SERVER 
## (Без контейнера)

## Предварительные требования

1. **Установите Python**
   Убедитесь, что у вас установлен Python (рекомендуемая версия: 3.8 или выше).

2. **Установите PostgreSQL**  
   Если __PostgreSQL__ еще не установлен, загрузите и установите его с [официального сайта](https://www.postgresql.org/download/).
3. Выполните следующие шаги используя свои данные для создания базы данных и пользователя:

   ```sql
   ALTER USER db_user CREATEDB;
   CREATE DATABASE my_db;
   CREATE USER db_user WITH PASSWORD '!!!!!!!!!password';
   GRANT ALL PRIVILEGES ON DATABASE gorder_db TO db_user;
   ALTER DATABASE your_db_name OWNER TO db_user;
    ```
## Зависимости

1. **Создайте и активируйте виртуальное окружение для управления зависимостями**

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate     # Для Windows
```
1. **Установите зависимости из requirements.txt**

```bash
pip install -r requirements.txt
```
## Настройка конфигурации
1. **Создайте файл .env**\
В корневой директории проекта создайте файл __.env__ и добавьте следующие настройки:

```plaintext
DB_NAME=my_db
DB_USER=db_user
DB_PASSWORD=my_password
DB_HOST=localhost
DB_PORT=5432
ENC_KEY=ваш_сгенерированный_ключ
```
2. **Сгенерируйте ENC_KEY**\
Для __ENC_KEY__, который используется в EncryptedCharField для шифрования данных, выполните следующий код в Python Console:

```python
from cryptography.fernet import Fernet

# Генерация ключа
key = Fernet.generate_key()
print(key.decode())  # Выводит ключ в виде строки
```
Скопируйте сгенерированный ключ и вставьте его в __.env__ файл в строку __ENC_KEY__.
3. **Примените миграции**\
Выполните миграции для создания всех необходимых таблиц в базе данных:
```bash
python manage.py migrate
```
## Запуск проекта
Теперь вы готовы запустить проект:

```bash
python manage.py runserver
```
Проект будет доступен по адресу __http://127.0.0.1:8000/__.
