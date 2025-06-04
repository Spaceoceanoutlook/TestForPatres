import psycopg2
from psycopg2 import sql
import psycopg2.errors

def create_db_and_user():
    admin_conn_params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": 5432,
    }

    new_db = "library_db"
    new_user = "library_user"
    new_password = "library_pass123"

    try:
        admin_conn = psycopg2.connect(**admin_conn_params)
        admin_conn.autocommit = True
        admin_cur = admin_conn.cursor()

        try:
            admin_cur.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(new_db)
                )
            )
            print(f"База '{new_db}' создана")
        except psycopg2.errors.DuplicateDatabase:
            print(f"База '{new_db}' уже существует")
        finally:
            admin_cur.close()
            admin_conn.close()

        # Подключаемся к новой БД
        new_db_conn_params = {
            "dbname": new_db,
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": 5432,
        }

        with psycopg2.connect(**new_db_conn_params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                            sql.Identifier(new_user)
                        ),
                        [new_password]
                    )
                    print(f"Пользователь '{new_user}' создан")
                except psycopg2.errors.DuplicateObject:
                    print(f"Пользователь '{new_user}' уже существует")

                # Права на БД
                grant_query = sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                    sql.Identifier(new_db),
                    sql.Identifier(new_user))
                cur.execute(grant_query)
                print(f"Права на '{new_db}' выданы '{new_user}'")

                # Права на схему public
                grant_schema_query = sql.SQL("GRANT ALL PRIVILEGES ON SCHEMA public TO {}").format(
                    sql.Identifier(new_user))
                cur.execute(grant_schema_query)
                print(f"Права на схему 'public' выданы '{new_user}'")

    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    create_db_and_user()
