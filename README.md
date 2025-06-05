## Настройка проекта

### 1. Создание и активация виртуального окружения

`poetry install`

`poetry shell`

### 2. Создание БД

#### Если Postgres установлен локально, то запустить скрипт `create_db.py`
#### Если Postgres не установлен, но установлен Docker, то ввести в терминале
`docker run --name my_postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres`
и далее запустить скрипт `create_db.py`

### 3. Применить миграции 
`alembic upgrade head`
