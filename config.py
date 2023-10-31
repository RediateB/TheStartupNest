import os
from datetime import timedelta

import flask

flask.cli.load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CORS_HEADERS = "Content-Type"
    # SESSION_COOKIE_SECURE = True
    # SESSION_COOKIE_SAMESITE = 'None'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('DATABASE_USERNAME')}:" \
                              f"{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_HOST')}:" \
                              f"{os.environ.get('DATABASE_PORT')}/{os.environ.get('APP_DATABASE')}"
