import os
from dotenv import load_dotenv

load_dotenv()


class SQLiteConfig:
    name = os.getenv('dbname', 'db.sqlite')
    url = rf'sqlite:///{name}'


class PostgresConfig:
    name = os.getenv('POSTGRES_DB', 'faces')
    user = os.getenv('POSTGRES_USER', 'user1')
    password = os.getenv('POSTGRES_PASSWORD', 'qwerty')
    host = os.getenv('POSTGRES_HOST', '0.0.0.0')
    port = os.getenv('POSTGRES_PORT', '5432')
    url = rf'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
