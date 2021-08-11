from flask import Flask

from configs.config import ApplicationConfig
from context import Context
from hooks import init_db_sqlite
from transport.flask.routes import get_routes


def configure_app(config: ApplicationConfig, context: Context):

    init_db_sqlite(config, context)

    app = Flask(__name__)

    for handler in get_routes(config, context):
        app.add_url_rule(
            rule=handler.uri,
            view_func=handler,
            methods=handler.methods
        )

    return app
