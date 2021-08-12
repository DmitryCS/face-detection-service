import os

from configs.config import ApplicationConfig
from context import Context
from recognize_video import main_predict_video
from transport.flask.configure_flask import configure_app
import multiprocessing


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
    mainpid = os.fork()
    if mainpid == 0:
        for _ in range(multiprocessing.cpu_count()):
            newpid = os.fork()
            if newpid == 0:
                main_predict_video()
    else:
        main()
