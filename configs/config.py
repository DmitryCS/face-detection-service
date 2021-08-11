from db.config import SQLiteConfig, PostgresConfig
from transport.flask.config import FlaskConfig


class ApplicationConfig:
    sanic: FlaskConfig
    # database: PostgresConfig
    database: SQLiteConfig

    def __init__(self):
        self.sanic = FlaskConfig()
        self.database = SQLiteConfig()
        # self.database = PostgresConfig()
