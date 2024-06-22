import psycopg2
import psycopg2.extras
from config_data.config import DatabaseConfig, connect_database
db_config: DatabaseConfig = connect_database()


def get_one_column(user_id: int, column_name: str) -> str | None:
    with psycopg2.connect(database=db_config.db.database_name, user=db_config.db.user, password=db_config.db.password,
                          host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT {column_name} '
                       f'FROM users '
                       f'WHERE id={user_id}')
        try:
            return cursor.fetchone()[0]
        except:
            return None


def get_several_columns(user_id: int, *column_names: str) -> dict | None:
    columns = ", ".join(column_names)
    with psycopg2.connect(database=db_config.db.database_name, user=db_config.db.user, password=db_config.db.password,
                          host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(f'SELECT {columns} '
                       f'FROM users '
                       f'WHERE id = {user_id}')
        try:
            result: dict
            for row in cursor:
                result = dict(row)
            return result
        except:
            return None


def insert_new_user(user_id: int) -> None:
    with psycopg2.connect(database=db_config.db.database_name, user=db_config.db.user, password=db_config.db.password,
                          host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO users (id, total_games, won) '
                       f'VALUES ({user_id}, 0, 0)')


def delete_user(user_id: int) -> None:
    with psycopg2.connect(database=db_config.db.database_name, user=db_config.db.user, password=db_config.db.password,
                          host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM users '
                       f'WHERE id = {user_id}')


def get_all_rows() -> list:
    with psycopg2.connect(database=db_config.db.database_name, user=db_config.db.user, password=db_config.db.password,
                          host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * '
                       f'FROM users')
        return cursor.fetchall()


def update_column(user_id: int, column_name: str, value: str | int) -> None:
    with psycopg2.connect(database=db_config.db.database_name, user=db_config.db.user, password=db_config.db.password,
                          host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor()
        cursor.execute(f'UPDATE users '
                       f'SET {column_name} = {value} '
                       f'WHERE id = {user_id}')


def get_stats(user_id: int) -> str | None:
    with psycopg2.connect(database=db_config.db.database_name, user=db_config.db.user, password=db_config.db.password,
                          host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(f'SELECT total_games, won '
                       f'FROM users '
                       f'WHERE id = {user_id}')
        result: dict
        for row in cursor:
            result = dict(row)
        print(result)
        return str(f'Всего игр: {result['total_games']}\n'
                       f'Побед: {result['won']}\n'
                       f'Процент побед: {round(result['total_games']/result['won'], 2)}')



def is_user_in_database(user_id: int) -> bool:
    with psycopg2.connect(database=db_config.db.database_name, user=db_config.db.user, password=db_config.db.password,
                          host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * '
                       f'FROM users '
                       f'WHERE id = {user_id}')
        if cursor.fetchone():
            return True
        else:
            return False
