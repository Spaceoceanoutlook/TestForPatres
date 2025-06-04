import psycopg2
from psycopg2 import sql

# Параметры подключения
ADMIN_CONN_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}

# Новая БД и пользователь
NEW_DB = "library_db"
NEW_USER = "library_user"
NEW_PASSWORD = "library_pass123"


def create_database(conn, db_name):
    with conn.cursor() as cur:
        try:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"База данных '{db_name}' создана.")
        except psycopg2.Error as e:
            if e.pgcode == "42P04":
                print(f"База данных '{db_name}' уже существует.")
            else:
                raise


def create_user_and_grant_privileges(admin_params, db_name, user, password):
    # Подключение к системной БД для создания пользователя
    with psycopg2.connect(**admin_params) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute(
                    sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(user)),
                    [password],
                )
                print(f"Пользователь '{user}' создан.")
            except psycopg2.Error as e:
                if e.pgcode == "42710":
                    print(f"Пользователь '{user}' уже существует.")
                else:
                    raise

            cur.execute(
                sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
                    sql.Identifier(db_name),
                    sql.Identifier(user)
                )
            )
            print(f"Права на подключение к БД '{db_name}' выданы пользователю '{user}'.")

    # Подключение к целевой БД для прав на схему
    db_params = admin_params.copy()
    db_params["dbname"] = db_name

    with psycopg2.connect(**db_params) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("GRANT ALL PRIVILEGES ON SCHEMA public TO {}").format(
                    sql.Identifier(user)
                )
            )
            print(f"Права на схему 'public' выданы пользователю '{user}'.")


def create_db_and_user():
    try:
        admin_conn = psycopg2.connect(**ADMIN_CONN_PARAMS)
        admin_conn.autocommit = True
        try:
            create_database(admin_conn, NEW_DB)
        finally:
            admin_conn.close()

        create_user_and_grant_privileges(ADMIN_CONN_PARAMS, NEW_DB, NEW_USER, NEW_PASSWORD)

    except psycopg2.OperationalError as e:
        print(f"[ОШИБКА ПОДКЛЮЧЕНИЯ] {e}")
    except Exception as e:
        print(f"[НЕОЖИДАННАЯ ОШИБКА] {e}")


if __name__ == "__main__":
    create_db_and_user()
