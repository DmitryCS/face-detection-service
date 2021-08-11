from configs.config import ApplicationConfig
from context import Context
from transport.flask.configure_flask import configure_app


def main():
    config = ApplicationConfig()
    context = Context()
    app = configure_app(config, context)
    app.run(
        host=config.sanic.host,
        port=config.sanic.port,
        debug=config.sanic.debug,
    )


if __name__ == "__main__":
    main()
