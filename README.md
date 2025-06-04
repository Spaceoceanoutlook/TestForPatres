Создание базы данных в Postgres.

Если Postgres установлен локально, то запустить скрипт create_db.py.

Если Postgres не установлен, но установлен Docker, то ввести в терминале

docker run --name my_postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

и после запустить скрипт create_db.py.
