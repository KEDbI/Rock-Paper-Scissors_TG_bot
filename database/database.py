import psycopg2
from config_data.config import DatabaseConfig, connect_database
db_config: DatabaseConfig = connect_database()
try:
    with psycopg2.connect(database='rock_paper_scissors', user=db_config.db.user, password=db_config.db.password,
        host=db_config.db.host, port=db_config.db.port) as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE users('
                           'id int NOT NULL,'
                           'total_games int,'
                           'won int,'
                           'lost int,'
                           'win_percentage int,'
                           'PRIMARY KEY(id))')
except:
    print("не получилось((")