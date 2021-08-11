import os
from dotenv import load_dotenv

load_dotenv()


class FlaskConfig:

    host = os.getenv('host', 'localhost')
    port = int(os.getenv('port', 8000))
    debug = bool(os.getenv('debug', False))
