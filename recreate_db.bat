@echo off

:: Удаляем базу данных, если она существует
psql -U postgres -d postgres -c "DROP DATABASE IF EXISTS gorder_db;"

:: Создаем базу данных
psql -U postgres -d postgres -c "CREATE DATABASE gorder_db;"

:: Предоставляем все права пользователю db_user
psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE gorder_db TO db_user;"

:: Изменяем владельца базы данных
psql -U postgres -d postgres -c "ALTER DATABASE gorder_db OWNER TO db_user;"

echo Database reset completed successfully.
pause